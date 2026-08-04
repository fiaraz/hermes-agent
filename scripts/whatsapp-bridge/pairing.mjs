import { makeWASocket, useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } from '@whiskeysockets/baileys';
import path from 'path';
import { fileURLToPath } from 'url';
import pino from 'pino';
import { mkdirSync } from 'fs';

const SESSION_DIR = path.join(process.env.HOME, '.hermes', 'whatsapp', 'session');
const PHONE_NUMBER = '447760257814';

// Ensure session dir exists
mkdirSync(SESSION_DIR, { recursive: true });

async function start() {
  const { version, isLatest } = await fetchLatestBaileysVersion();
  const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);

  const sock = makeWASocket({
    version,
    auth: state,
    logger: pino({ level: 'silent' }),
    printQRInTerminal: false,
    browser: ['Chrome (Linux)', '', ''],
  });

  sock.ev.on('creds.update', saveCreds);

  // Wait a moment for the socket to initialize, then request pairing code
  setTimeout(async () => {
    try {
      const code = await sock.requestPairingCode(PHONE_NUMBER);
      // Format the code with spaces for readability
      const formatted = code.match(/.{1,4}/g).join('-');
      console.log('\n==============================');
      console.log('WHATSAPP PAIRING CODE:');
      console.log(`  ${formatted}`);
      console.log('==============================');
      console.log('\nOn your phone:');
      console.log('1. Open WhatsApp');
      console.log('2. Tap the 3 dots (or settings gear)');
      console.log('3. Linked Devices > Link a Device');
      console.log('4. Tap "Link with phone number instead"');
      console.log(`5. Enter: ${formatted}`);
      console.log('\nWaiting for connection...\n');
    } catch (err) {
      console.error('Failed to get pairing code:', err.message);
    }
  }, 5000);

  sock.ev.on('connection.update', (update) => {
    const { connection, lastDisconnect } = update;
    if (connection === 'open') {
      console.log('WhatsApp connected successfully!');
      process.exit(0);
    } else if (connection === 'close') {
      const reason = lastDisconnect?.error?.output?.statusCode;
      if (reason === DisconnectReason.loggedOut) {
        console.log('Logged out. Re-run for a fresh pairing code.');
        process.exit(1);
      } else {
        console.log('Disconnected, reconnecting...');
      }
    }
  });
}

start();
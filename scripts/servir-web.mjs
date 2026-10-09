// Servidor estático mínimo para os testes de ponta a ponta: serve a pasta dist (expo export --platform web)
// e devolve o index.html para qualquer rota, como o app web espera (rotas do Expo Router).
import { createServer } from 'node:http';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';

const raiz = join(process.cwd(), 'dist');
const porta = Number(process.env.PORT ?? 4173);
const tipos = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.png': 'image/png', '.ico': 'image/x-icon', '.svg': 'image/svg+xml', '.wasm': 'application/wasm', '.ttf': 'font/ttf' };

createServer((req, res) => {
  const caminho = normalize(decodeURIComponent(req.url.split('?')[0])).replace(/^(\.\.[/\\])+/, '');
  let arquivo = join(raiz, caminho);
  if (!existsSync(arquivo) || statSync(arquivo).isDirectory()) arquivo = join(raiz, 'index.html');
  res.setHeader('content-type', tipos[extname(arquivo)] ?? 'application/octet-stream');
  res.end(readFileSync(arquivo));
}).listen(porta, () => console.log(`PyPasso web em http://localhost:${porta}`));

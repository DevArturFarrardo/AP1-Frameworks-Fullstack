// Funções que falam com o backend Flask.
// Todas chamam endpoints "/api/..." que são redirecionados para
// http://localhost:5000 pelo proxy do Vite (vite.config.js).
//
// Use sempre estas funções nos componentes — assim, se um dia
// trocar a URL do backend, só precisa alterar este arquivo.

// Pega o token JWT salvo no navegador (ou null se não houver).
function getToken() {
  return localStorage.getItem("token");
}

// Função base que faz uma requisição HTTP para o backend.
// - method: "GET", "POST", "PUT", "PATCH"
// - body:   objeto JS que vira JSON (ou undefined se não tiver corpo)
// - auth:   se true, anexa o token JWT no header Authorization
async function request(url, { method = "GET", body, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  let data = null;
  const text = await res.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { raw: text };
    }
  }

  if (!res.ok) {
    const msg = data?.erro || data?.msg || `Erro ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

// ===== Sellers =====
export const cadastrarSeller = (dados) =>
  request("/api/sellers", { method: "POST", body: dados });

export const ativarSeller = (celular, codigo) =>
  request("/api/sellers/activate", { method: "POST", body: { celular, codigo } });

export const loginSeller = (email, senha) =>
  request("/api/sellers/login", { method: "POST", body: { email, senha } });

// ===== Produtos =====
export const listarProdutos = () =>
  request("/api/products", { auth: true });

export const criarProduto = (dados) =>
  request("/api/products", { method: "POST", body: dados, auth: true });

export const editarProduto = (id, dados) =>
  request(`/api/products/${id}`, { method: "PUT", body: dados, auth: true });

export const inativarProduto = (id) =>
  request(`/api/products/${id}/inactivate`, { method: "PATCH", auth: true });

// ===== Vendas =====
export const listarVendas = () =>
  request("/api/sales", { auth: true });

export const criarVenda = (produtoId, quantidade) =>
  request("/api/sales", {
    method: "POST",
    body: { produtoId, quantidade },
    auth: true,
  });

// ===== Upload de imagem =====
// Envia o arquivo selecionado pelo usuário (multipart/form-data) e
// devolve um objeto `{ url, filename }`. Use `url` no campo `img`
// do produto.
export async function uploadImagemProduto(arquivo) {
  const token = localStorage.getItem("token");
  const formData = new FormData();
  formData.append("file", arquivo);

  const res = await fetch("/api/uploads/product-image", {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: formData,
  });

  let data = null;
  const text = await res.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { raw: text };
    }
  }
  if (!res.ok) {
    const msg = data?.erro || `Erro ${res.status} ao enviar imagem`;
    throw new Error(msg);
  }
  return data;
}

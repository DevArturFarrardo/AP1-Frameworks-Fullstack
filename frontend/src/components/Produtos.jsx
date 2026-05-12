import { useState, useEffect } from "react";
import {
  listarProdutos,
  criarProduto,
  editarProduto,
  inativarProduto,
  uploadImagemProduto,
} from "../api.js";

// Página de produtos: lista, cadastra, edita, vê detalhes e inativa.
// useState guarda:
//   - produtos: array de produtos vindos da API
//   - mostrarForm: se o formulário (modal) deve aparecer
//   - emEdicao: produto sendo editado (null = cadastro novo)
//   - form: dados digitados no formulário
//   - arquivoImagem: File selecionado pelo usuário (ou null)
//   - previewImagem: URL local (blob:) para mostrar a imagem antes de salvar
//   - enviando: true enquanto faz upload + salvar
//   - erro: mensagem de erro a exibir
//   - produtoDetalhe: produto aberto na tela de detalhes (ou null)
export default function Produtos() {
  const [produtos, setProdutos] = useState([]);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [emEdicao, setEmEdicao] = useState(null);
  const [form, setForm] = useState({
    nome: "",
    preco: "",
    quantidade: "",
    img: "",
    status: "Ativo",
  });
  const [arquivoImagem, setArquivoImagem] = useState(null);
  const [previewImagem, setPreviewImagem] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState("");
  const [produtoDetalhe, setProdutoDetalhe] = useState(null);

  // Quando o componente abre, busca a lista de produtos.
  useEffect(() => {
    carregar();
  }, []);

  async function carregar() {
    try {
      const resp = await listarProdutos();
      setProdutos(resp.produtos || []);
    } catch (err) {
      setErro(err.message);
    }
  }

  function abrirNovo() {
    setEmEdicao(null);
    setForm({ nome: "", preco: "", quantidade: "", img: "", status: "Ativo" });
    setArquivoImagem(null);
    setPreviewImagem("");
    setErro("");
    setMostrarForm(true);
  }

  function abrirEdicao(produto) {
    setEmEdicao(produto);
    setForm({
      nome: produto.nome,
      preco: produto.preco,
      quantidade: produto.quantidade,
      img: produto.img || "",
      status: produto.status,
    });
    setArquivoImagem(null);
    setPreviewImagem(produto.img || "");
    setErro("");
    setMostrarForm(true);
  }

  // Quando o usuário escolhe uma imagem no input type="file":
  // - guardamos o File em arquivoImagem (vai ser enviado ao salvar)
  // - geramos um blob URL com URL.createObjectURL para mostrar preview
  function aoEscolherArquivo(e) {
    const arq = e.target.files?.[0];
    if (!arq) {
      setArquivoImagem(null);
      setPreviewImagem(emEdicao?.img || "");
      return;
    }
    setArquivoImagem(arq);
    setPreviewImagem(URL.createObjectURL(arq));
  }

  async function salvar(e) {
    e.preventDefault();
    setErro("");
    setEnviando(true);
    try {
      // 1) Se o usuário escolheu um arquivo novo, faz upload primeiro
      //    e usa a URL devolvida no campo img.
      let urlImagem = form.img || null;
      if (arquivoImagem) {
        const resp = await uploadImagemProduto(arquivoImagem);
        urlImagem = resp.url;
      }

      const dados = {
        nome: form.nome,
        preco: parseFloat(form.preco),
        quantidade: parseInt(form.quantidade, 10),
        img: urlImagem,
      };

      if (emEdicao) {
        await editarProduto(emEdicao.id, { ...dados, status: form.status });
      } else {
        await criarProduto(dados);
      }
      setMostrarForm(false);
      await carregar();
    } catch (err) {
      setErro(err.message);
    } finally {
      setEnviando(false);
    }
  }

  async function inativar(produto) {
    if (!window.confirm(`Inativar o produto "${produto.nome}"?`)) return;
    try {
      await inativarProduto(produto.id);
      await carregar();
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Produtos</h2>
          <p>Cadastre, edite e inative os itens do seu estoque.</p>
        </div>
        <button className="btn-primary" onClick={abrirNovo}>
          + Novo produto
        </button>
      </div>

      {produtos.length === 0 && (
        <div className="empty">
          Nenhum produto cadastrado ainda. Clique em <strong>Novo produto</strong>.
        </div>
      )}

      <div className="cards-grid">
        {produtos.map((p) => (
          <article key={p.id} className="product-card">
            <div className="product-img">
              {p.img ? <img src={p.img} alt={p.nome} /> : "📦"}
            </div>
            <div className="product-body">
              <h3>{p.nome}</h3>
              <span
                className={
                  p.status === "Ativo"
                    ? "badge badge-ativo"
                    : "badge badge-inativo"
                }
              >
                {p.status}
              </span>
              <div className="product-meta">
                <div className="product-price">
                  {Number(p.preco).toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                  })}
                </div>
                <div className="product-stock">
                  Estoque: <strong>{p.quantidade}</strong>
                </div>
              </div>
            </div>
            <div className="product-actions">
              <button onClick={() => setProdutoDetalhe(p)}>Detalhes</button>
              <button onClick={() => abrirEdicao(p)}>Editar</button>
              <button
                className="danger"
                onClick={() => inativar(p)}
                disabled={p.status !== "Ativo"}
              >
                Inativar
              </button>
            </div>
          </article>
        ))}
      </div>

      {/* ===== Modal de cadastro / edição ===== */}
      {mostrarForm && (
        <div className="modal" onClick={() => setMostrarForm(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <header className="modal-header">
              <h3>{emEdicao ? "Editar produto" : "Novo produto"}</h3>
              <button
                className="btn-icon"
                onClick={() => setMostrarForm(false)}
              >
                ×
              </button>
            </header>
            <form className="modal-body" onSubmit={salvar}>
              <label>
                <span>Nome</span>
                <input
                  type="text"
                  required
                  value={form.nome}
                  onChange={(e) => setForm({ ...form, nome: e.target.value })}
                />
              </label>
              <label>
                <span>Preço (R$)</span>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  value={form.preco}
                  onChange={(e) => setForm({ ...form, preco: e.target.value })}
                />
              </label>
              <label>
                <span>Quantidade em estoque</span>
                <input
                  type="number"
                  step="1"
                  min="0"
                  required
                  value={form.quantidade}
                  onChange={(e) =>
                    setForm({ ...form, quantidade: e.target.value })
                  }
                />
              </label>

              <label>
                <span>
                  Imagem do produto{" "}
                  <small>(PNG, JPG, GIF, WEBP — até 5 MB)</small>
                </span>
                <input
                  type="file"
                  accept="image/png,image/jpeg,image/jpg,image/gif,image/webp"
                  onChange={aoEscolherArquivo}
                />
              </label>

              {previewImagem && (
                <div className="image-preview">
                  <img src={previewImagem} alt="Pré-visualização" />
                  {arquivoImagem && (
                    <span className="hint">
                      Selecionado: {arquivoImagem.name}
                    </span>
                  )}
                </div>
              )}

              {emEdicao && (
                <label>
                  <span>Status</span>
                  <select
                    value={form.status}
                    onChange={(e) =>
                      setForm({ ...form, status: e.target.value })
                    }
                  >
                    <option value="Ativo">Ativo</option>
                    <option value="Inativo">Inativo</option>
                  </select>
                </label>
              )}

              {erro && <div className="erro">{erro}</div>}

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-ghost"
                  onClick={() => setMostrarForm(false)}
                  disabled={enviando}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn-primary"
                  disabled={enviando}
                >
                  {enviando
                    ? "Enviando..."
                    : emEdicao
                    ? "Salvar"
                    : "Cadastrar"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ===== Modal de detalhes do produto ===== */}
      {produtoDetalhe && (
        <div className="modal" onClick={() => setProdutoDetalhe(null)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <header className="modal-header">
              <h3>Detalhes do produto</h3>
              <button
                className="btn-icon"
                onClick={() => setProdutoDetalhe(null)}
              >
                ×
              </button>
            </header>
            <div className="modal-body detalhes">
              <div className="detalhes-img">
                {produtoDetalhe.img ? (
                  <img src={produtoDetalhe.img} alt={produtoDetalhe.nome} />
                ) : (
                  <span>📦</span>
                )}
              </div>
              <dl className="detalhes-dados">
                <dt>ID</dt>
                <dd>#{produtoDetalhe.id}</dd>
                <dt>Nome</dt>
                <dd>{produtoDetalhe.nome}</dd>
                <dt>Preço</dt>
                <dd>
                  {Number(produtoDetalhe.preco).toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                  })}
                </dd>
                <dt>Estoque</dt>
                <dd>{produtoDetalhe.quantidade}</dd>
                <dt>Status</dt>
                <dd>
                  <span
                    className={
                      produtoDetalhe.status === "Ativo"
                        ? "badge badge-ativo"
                        : "badge badge-inativo"
                    }
                  >
                    {produtoDetalhe.status}
                  </span>
                </dd>
              </dl>
              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-ghost"
                  onClick={() => setProdutoDetalhe(null)}
                >
                  Fechar
                </button>
                <button
                  type="button"
                  className="btn-primary"
                  onClick={() => {
                    setProdutoDetalhe(null);
                    abrirEdicao(produtoDetalhe);
                  }}
                >
                  Editar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

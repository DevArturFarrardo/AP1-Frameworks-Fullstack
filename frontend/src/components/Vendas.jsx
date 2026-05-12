import { useState, useEffect } from "react";
import { listarVendas, listarProdutos, criarVenda } from "../api.js";

// Página de vendas: lista, mostra KPIs e cria nova venda.
// useState guarda:
//   - vendas: lista vinda da API
//   - produtos: lista para escolher na hora de vender
//   - mostrarForm: se o modal de "nova venda" está aberto
//   - produtoId: produto escolhido no formulário
//   - quantidade: quantidade digitada
//   - erro: mensagem de erro
export default function Vendas() {
  const [vendas, setVendas] = useState([]);
  const [produtos, setProdutos] = useState([]);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [produtoId, setProdutoId] = useState("");
  const [quantidade, setQuantidade] = useState(1);
  const [erro, setErro] = useState("");

  useEffect(() => {
    carregar();
  }, []);

  async function carregar() {
    try {
      const [v, p] = await Promise.all([listarVendas(), listarProdutos()]);
      setVendas(v.vendas || []);
      setProdutos(p.produtos || []);
    } catch (err) {
      setErro(err.message);
    }
  }

  // Lista só de produtos ativos com estoque > 0 (válidos para venda).
  const produtosVendaveis = produtos.filter(
    (p) => p.status === "Ativo" && p.quantidade > 0
  );

  function abrirForm() {
    setErro("");
    setProdutoId(produtosVendaveis[0]?.id ?? "");
    setQuantidade(1);
    setMostrarForm(true);
  }

  async function salvar(e) {
    e.preventDefault();
    setErro("");
    try {
      await criarVenda(Number(produtoId), Number(quantidade));
      setMostrarForm(false);
      await carregar();
    } catch (err) {
      setErro(err.message);
    }
  }

  // Cálculos rápidos para os KPIs.
  const totalVendas = vendas.length;
  const receita = vendas.reduce((acc, v) => acc + Number(v.total || 0), 0);
  const itens = vendas.reduce((acc, v) => acc + Number(v.quantidade || 0), 0);

  // Função auxiliar para descobrir o nome do produto pelo id.
  function nomeProduto(id) {
    const p = produtos.find((x) => x.id === id);
    return p ? p.nome : `Produto ${id}`;
  }

  // Pré-visualização do total dentro do formulário.
  const produtoSelecionado = produtos.find((p) => p.id === Number(produtoId));
  const previewTotal = produtoSelecionado
    ? produtoSelecionado.preco * Number(quantidade || 0)
    : 0;

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Vendas</h2>
          <p>Registre uma venda e acompanhe o histórico.</p>
        </div>
        <button
          className="btn-primary"
          onClick={abrirForm}
          disabled={produtosVendaveis.length === 0}
        >
          + Nova venda
        </button>
      </div>

      <div className="kpis">
        <div className="kpi">
          <span>Total de vendas</span>
          <strong>{totalVendas}</strong>
        </div>
        <div className="kpi">
          <span>Receita acumulada</span>
          <strong>
            {receita.toLocaleString("pt-BR", {
              style: "currency",
              currency: "BRL",
            })}
          </strong>
        </div>
        <div className="kpi">
          <span>Itens vendidos</span>
          <strong>{itens}</strong>
        </div>
      </div>

      {vendas.length === 0 ? (
        <div className="empty">Nenhuma venda registrada ainda.</div>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Produto</th>
                <th>Qtde</th>
                <th>Preço unit.</th>
                <th>Total</th>
                <th>Data</th>
              </tr>
            </thead>
            <tbody>
              {vendas.map((v) => (
                <tr key={v.id}>
                  <td>#{v.id}</td>
                  <td>{nomeProduto(v.produto_id)}</td>
                  <td>{v.quantidade}</td>
                  <td>
                    {Number(v.preco_unitario).toLocaleString("pt-BR", {
                      style: "currency",
                      currency: "BRL",
                    })}
                  </td>
                  <td>
                    <strong>
                      {Number(v.total).toLocaleString("pt-BR", {
                        style: "currency",
                        currency: "BRL",
                      })}
                    </strong>
                  </td>
                  <td>
                    {v.created_at
                      ? new Date(v.created_at).toLocaleString("pt-BR")
                      : "-"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {mostrarForm && (
        <div className="modal" onClick={() => setMostrarForm(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <header className="modal-header">
              <h3>Nova venda</h3>
              <button
                className="btn-icon"
                onClick={() => setMostrarForm(false)}
              >
                ×
              </button>
            </header>
            <form className="modal-body" onSubmit={salvar}>
              <label>
                <span>Produto</span>
                <select
                  required
                  value={produtoId}
                  onChange={(e) => setProdutoId(e.target.value)}
                >
                  {produtosVendaveis.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.nome} —{" "}
                      {Number(p.preco).toLocaleString("pt-BR", {
                        style: "currency",
                        currency: "BRL",
                      })}{" "}
                      (estoque {p.quantidade})
                    </option>
                  ))}
                </select>
              </label>
              <label>
                <span>Quantidade</span>
                <input
                  type="number"
                  min="1"
                  step="1"
                  required
                  value={quantidade}
                  onChange={(e) => setQuantidade(e.target.value)}
                />
              </label>

              <p className="hint">
                Total:{" "}
                {previewTotal.toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                })}
              </p>

              {erro && <div className="erro">{erro}</div>}

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-ghost"
                  onClick={() => setMostrarForm(false)}
                >
                  Cancelar
                </button>
                <button type="submit" className="btn-primary">
                  Registrar venda
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </section>
  );
}

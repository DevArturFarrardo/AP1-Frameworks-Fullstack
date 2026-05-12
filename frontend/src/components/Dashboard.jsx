import { useState, useEffect } from "react";
import { listarProdutos, listarVendas } from "../api.js";

// Tela de Dashboard: painel com relatórios e indicadores em tempo real.
// useState guarda:
//   - produtos: lista atual de produtos (para calcular estoque)
//   - vendas:   lista atual de vendas   (para calcular receita)
//   - erro:     mensagem de erro caso a API falhe
//   - carregando: enquanto busca dados
//
// useEffect chama carregar() ao abrir a tela. Isso garante o
// "monitoramento de estoque em tempo real" toda vez que o seller
// abrir o dashboard.
export default function Dashboard() {
  const [produtos, setProdutos] = useState([]);
  const [vendas, setVendas] = useState([]);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    carregar();
  }, []);

  async function carregar() {
    setErro("");
    setCarregando(true);
    try {
      const [p, v] = await Promise.all([listarProdutos(), listarVendas()]);
      setProdutos(p.produtos || []);
      setVendas(v.vendas || []);
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  // ===== Cálculos dos indicadores (requisitos da P2) =====

  // Indicador 1: quantidade total de produtos em estoque
  // (soma da quantidade de TODOS os produtos cadastrados).
  const quantidadeEmEstoque = produtos.reduce(
    (acc, p) => acc + Number(p.quantidade || 0),
    0
  );

  // Indicador 2: valor total vendido (soma do campo total de cada venda).
  const valorTotalVendido = vendas.reduce(
    (acc, v) => acc + Number(v.total || 0),
    0
  );

  // ===== Indicadores adicionais (úteis no relatório) =====
  const totalProdutosCadastrados = produtos.length;
  const produtosAtivos = produtos.filter((p) => p.status === "Ativo").length;
  const produtosSemEstoque = produtos.filter((p) => p.quantidade === 0).length;
  const totalVendas = vendas.length;
  const itensVendidos = vendas.reduce(
    (acc, v) => acc + Number(v.quantidade || 0),
    0
  );

  // Top 5 produtos com maior estoque (para o painel de estoque).
  const topEstoque = [...produtos]
    .sort((a, b) => b.quantidade - a.quantidade)
    .slice(0, 5);

  // Produtos com estoque baixo (<= 5) e ativos — alerta para o seller.
  const estoqueBaixo = produtos.filter(
    (p) => p.status === "Ativo" && p.quantidade > 0 && p.quantidade <= 5
  );

  // Ranking dos produtos mais vendidos (por quantidade).
  const vendasPorProduto = {};
  for (const v of vendas) {
    const id = v.produto_id;
    if (!vendasPorProduto[id]) {
      vendasPorProduto[id] = { quantidade: 0, total: 0 };
    }
    vendasPorProduto[id].quantidade += Number(v.quantidade || 0);
    vendasPorProduto[id].total += Number(v.total || 0);
  }
  const topVendidos = Object.entries(vendasPorProduto)
    .map(([id, d]) => {
      const prod = produtos.find((p) => p.id === Number(id));
      return {
        id: Number(id),
        nome: prod ? prod.nome : `Produto ${id}`,
        quantidade: d.quantidade,
        total: d.total,
      };
    })
    .sort((a, b) => b.quantidade - a.quantidade)
    .slice(0, 5);

  // Formata número como moeda brasileira (R$).
  function formatarMoeda(valor) {
    return Number(valor).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p>
            Painel com relatórios de vendas e monitoramento de estoque em tempo
            real.
          </p>
        </div>
        <button className="btn-ghost" onClick={carregar} disabled={carregando}>
          {carregando ? "Atualizando..." : "Atualizar"}
        </button>
      </div>

      {erro && <div className="erro">{erro}</div>}

      {/* ===== KPIs principais (indicadores exigidos pela P2) ===== */}
      <div className="kpis">
        <div className="kpi kpi-destaque">
          <span>Produtos em estoque</span>
          <strong>{quantidadeEmEstoque}</strong>
          <small>unidades disponíveis</small>
        </div>
        <div className="kpi kpi-destaque">
          <span>Valor total vendido</span>
          <strong>{formatarMoeda(valorTotalVendido)}</strong>
          <small>receita acumulada</small>
        </div>
      </div>

      {/* ===== KPIs complementares ===== */}
      <div className="kpis">
        <div className="kpi">
          <span>Produtos cadastrados</span>
          <strong>{totalProdutosCadastrados}</strong>
        </div>
        <div className="kpi">
          <span>Produtos ativos</span>
          <strong>{produtosAtivos}</strong>
        </div>
        <div className="kpi">
          <span>Sem estoque</span>
          <strong>{produtosSemEstoque}</strong>
        </div>
        <div className="kpi">
          <span>Total de vendas</span>
          <strong>{totalVendas}</strong>
        </div>
        <div className="kpi">
          <span>Itens vendidos</span>
          <strong>{itensVendidos}</strong>
        </div>
      </div>

      {/* ===== Alerta de estoque baixo ===== */}
      {estoqueBaixo.length > 0 && (
        <div className="dashboard-card alerta">
          <h3>Atenção: estoque baixo</h3>
          <p>Estes produtos estão com 5 unidades ou menos:</p>
          <ul className="lista-alerta">
            {estoqueBaixo.map((p) => (
              <li key={p.id}>
                <strong>{p.nome}</strong> — {p.quantidade} un.
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ===== Tabelas de relatório ===== */}
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Top produtos em estoque</h3>
          {topEstoque.length === 0 ? (
            <div className="empty">Nenhum produto cadastrado.</div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Produto</th>
                  <th>Status</th>
                  <th>Estoque</th>
                </tr>
              </thead>
              <tbody>
                {topEstoque.map((p) => (
                  <tr key={p.id}>
                    <td>{p.nome}</td>
                    <td>
                      <span
                        className={
                          p.status === "Ativo"
                            ? "badge badge-ativo"
                            : "badge badge-inativo"
                        }
                      >
                        {p.status}
                      </span>
                    </td>
                    <td>
                      <strong>{p.quantidade}</strong>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="dashboard-card">
          <h3>Produtos mais vendidos</h3>
          {topVendidos.length === 0 ? (
            <div className="empty">Nenhuma venda registrada ainda.</div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Produto</th>
                  <th>Qtde</th>
                  <th>Receita</th>
                </tr>
              </thead>
              <tbody>
                {topVendidos.map((v) => (
                  <tr key={v.id}>
                    <td>{v.nome}</td>
                    <td>{v.quantidade}</td>
                    <td>
                      <strong>{formatarMoeda(v.total)}</strong>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </section>
  );
}

import { useState } from "react";
import Login from "./components/Login.jsx";
import Cadastro from "./components/Cadastro.jsx";
import Ativacao from "./components/Ativacao.jsx";
import Produtos from "./components/Produtos.jsx";
import Vendas from "./components/Vendas.jsx";
import Dashboard from "./components/Dashboard.jsx";

// Componente principal da aplicação.
// Usa useState para guardar:
//   - seller: dados do mini mercado logado (ou null se não logado)
//   - telaAuth: qual aba mostrar antes do login (login | cadastro | ativacao)
//   - paginaApp: qual página mostrar depois do login (dashboard | produtos | vendas)
//   - mensagem: texto exibido no topo após cadastro/ativação
export default function App() {
  // Tenta recuperar um seller salvo no localStorage (se já estava logado).
  const sellerSalvo = JSON.parse(localStorage.getItem("seller") || "null");

  const [seller, setSeller] = useState(sellerSalvo);
  const [telaAuth, setTelaAuth] = useState("login");
  const [paginaApp, setPaginaApp] = useState("dashboard");
  const [mensagem, setMensagem] = useState("");

  // Chamado por <Login> quando o usuário entra com sucesso.
  function aoEntrar(dadosSeller, accessToken, refreshToken) {
    localStorage.setItem("token", accessToken);
    localStorage.setItem("refresh", refreshToken);
    localStorage.setItem("seller", JSON.stringify(dadosSeller));
    setSeller(dadosSeller);
    setMensagem("");
  }

  // Limpa tudo e volta para a tela de login.
  function sair() {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
    localStorage.removeItem("seller");
    setSeller(null);
    setTelaAuth("login");
  }

  // Caso o usuário NÃO esteja logado, mostra Login / Cadastro / Ativação.
  if (!seller) {
    return (
      <div className="auth-shell">
        <div className="auth-card">
          <header className="logo">
            <span className="logo-mark">MM</span>
            <div>
              <h1>Mini Mercado</h1>
              <p>Gestão de estoque & vendas</p>
            </div>
          </header>

          <nav className="tabs">
            <button
              className={telaAuth === "login" ? "tab active" : "tab"}
              onClick={() => setTelaAuth("login")}
            >
              Entrar
            </button>
            <button
              className={telaAuth === "cadastro" ? "tab active" : "tab"}
              onClick={() => setTelaAuth("cadastro")}
            >
              Cadastrar
            </button>
            <button
              className={telaAuth === "ativacao" ? "tab active" : "tab"}
              onClick={() => setTelaAuth("ativacao")}
            >
              Ativar conta
            </button>
          </nav>

          {mensagem && <div className="info-banner">{mensagem}</div>}

          {telaAuth === "login" && <Login aoEntrar={aoEntrar} />}
          {telaAuth === "cadastro" && (
            <Cadastro
              aoCadastrar={(msg) => {
                setMensagem(msg);
                setTelaAuth("ativacao");
              }}
            />
          )}
          {telaAuth === "ativacao" && (
            <Ativacao
              aoAtivar={() => {
                setMensagem("Conta ativada! Faça login para continuar.");
                setTelaAuth("login");
              }}
            />
          )}
        </div>

        <aside className="auth-side">
          <h2>Bem-vindo!</h2>
          <p>
            Gerencie produtos, estoque e vendas do seu mini mercado em um só
            lugar.
          </p>
          <ul>
            <li>Cadastro com ativação por WhatsApp</li>
            <li>Controle de estoque automático</li>
            <li>Histórico de vendas</li>
          </ul>
        </aside>
      </div>
    );
  }

  // Caso esteja logado: mostra layout do app (topbar + sidebar + página atual).
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="logo-mark small">MM</span>
          <strong>Mini Mercado</strong>
        </div>
        <div className="topbar-right">
          <span className="user-chip">{seller.nome}</span>
          <button className="btn-ghost" onClick={sair}>
            Sair
          </button>
        </div>
      </header>

      <nav className="sidenav">
        <button
          className={paginaApp === "dashboard" ? "navlink active" : "navlink"}
          onClick={() => setPaginaApp("dashboard")}
        >
          Dashboard
        </button>
        <button
          className={paginaApp === "produtos" ? "navlink active" : "navlink"}
          onClick={() => setPaginaApp("produtos")}
        >
          Produtos
        </button>
        <button
          className={paginaApp === "vendas" ? "navlink active" : "navlink"}
          onClick={() => setPaginaApp("vendas")}
        >
          Vendas
        </button>
      </nav>

      <main className="content">
        {paginaApp === "dashboard" && <Dashboard />}
        {paginaApp === "produtos" && <Produtos />}
        {paginaApp === "vendas" && <Vendas />}
      </main>
    </div>
  );
}

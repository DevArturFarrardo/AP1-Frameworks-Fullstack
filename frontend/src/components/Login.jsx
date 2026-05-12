import { useState } from "react";
import { loginSeller } from "../api.js";

// Tela de login.
// Usa useState para guardar o que o usuário digita nos campos
// e uma mensagem de erro caso o login falhe.
export default function Login({ aoEntrar }) {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function aoEnviar(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      const resp = await loginSeller(email, senha);
      aoEntrar(resp.seller, resp.access_token, resp.refresh_token);
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <form className="auth-form" onSubmit={aoEnviar}>
      <label>
        <span>E-mail</span>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="mercado@email.com"
        />
      </label>
      <label>
        <span>Senha</span>
        <input
          type="password"
          required
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          placeholder="••••••"
        />
      </label>

      {erro && <div className="erro">{erro}</div>}

      <button type="submit" className="btn-primary" disabled={carregando}>
        {carregando ? "Entrando..." : "Entrar"}
      </button>
    </form>
  );
}

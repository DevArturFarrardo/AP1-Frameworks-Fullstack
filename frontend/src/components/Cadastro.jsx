import { useState } from "react";
import { cadastrarSeller } from "../api.js";

// Tela de cadastro do mini mercado.
// Cada campo do formulário é controlado por um useState próprio.
export default function Cadastro({ aoCadastrar }) {
  const [nome, setNome] = useState("");
  const [cnpj, setCnpj] = useState("");
  const [email, setEmail] = useState("");
  const [celular, setCelular] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function aoEnviar(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      await cadastrarSeller({ nome, cnpj, email, celular, senha });

      // O código de ativação é enviado SOMENTE via WhatsApp pelo Twilio.
      // Por segurança, o backend não retorna o código para o cliente.
      aoCadastrar(
        "Cadastro realizado! Verifique o seu WhatsApp — enviamos um código de 4 dígitos para ativar a conta."
      );
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <form className="auth-form" onSubmit={aoEnviar}>
      <label>
        <span>Nome do mercado</span>
        <input
          type="text"
          required
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />
      </label>
      <label>
        <span>CNPJ</span>
        <input
          type="text"
          required
          value={cnpj}
          onChange={(e) => setCnpj(e.target.value)}
          placeholder="00.000.000/0001-00"
        />
      </label>
      <label>
        <span>E-mail</span>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </label>
      <label>
        <span>Celular (DDD + número)</span>
        <input
          type="tel"
          required
          value={celular}
          onChange={(e) => setCelular(e.target.value)}
          placeholder="11959913833"
        />
      </label>
      <label>
        <span>Senha</span>
        <input
          type="password"
          required
          minLength={4}
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
      </label>

      {erro && <div className="erro">{erro}</div>}

      <button type="submit" className="btn-primary" disabled={carregando}>
        {carregando ? "Cadastrando..." : "Criar conta"}
      </button>
    </form>
  );
}

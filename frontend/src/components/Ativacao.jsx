import { useState } from "react";
import { ativarSeller } from "../api.js";

// Tela de ativação da conta com o código de 4 dígitos.
export default function Ativacao({ aoAtivar }) {
  const [celular, setCelular] = useState("");
  const [codigo, setCodigo] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function aoEnviar(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      await ativarSeller(celular, codigo);
      aoAtivar();
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <form className="auth-form" onSubmit={aoEnviar}>
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
        <span>Código de 4 dígitos</span>
        <input
          type="text"
          required
          maxLength={4}
          value={codigo}
          onChange={(e) => setCodigo(e.target.value)}
          placeholder="1234"
        />
      </label>

      {erro && <div className="erro">{erro}</div>}

      <button type="submit" className="btn-primary" disabled={carregando}>
        {carregando ? "Ativando..." : "Ativar conta"}
      </button>
    </form>
  );
}

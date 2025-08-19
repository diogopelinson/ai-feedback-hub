import React, { useState } from 'react';
import '../styles/styles.css';

function FeedbackForm() {
  const [text, setText] = useState('');
  const [feedback, setFeedback] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setFeedback('');

    try {
      const res = await fetch(process.env.REACT_APP_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await res.json();
      setFeedback(data.feedback || data.error || 'Sem resposta');
    } catch (err) {
      setFeedback('Erro ao chamar a API');
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <h1 className="title">AI Feedback Hub</h1>
      <p className="subtitle">Envie seu texto e receba um feedback instantâneo da IA</p>

      <form onSubmit={handleSubmit} className="form">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows="6"
          placeholder="Digite seu texto aqui..."
        />
        <button type="submit" disabled={loading || !text.trim()}>
          {loading ? 'Enviando...' : 'Enviar'}
        </button>
      </form>

      {feedback && (
        <div className="feedback-box fade-in">
          <h3>Resultado</h3>
          <p>{feedback}</p>
        </div>
      )}
    </div>
  );
}

export default FeedbackForm;

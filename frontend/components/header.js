export default function Header() {
  return (
    <header className="header">
      <h1 className="title">
        Effectz VLM OCR
      </h1>
      <div className="right-section">
        <p className="built-by">
          Built by <a href="https://www.effectz.ai/" className="company-link">Effectz.AI</a>
        </p>
        <img src="/effectz.png" alt="Logo" className="logo" />
      </div>
    </header>
  );
}

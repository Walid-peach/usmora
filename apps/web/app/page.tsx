"use client";

import { FormEvent, useState } from "react";

type Reflection = {
  facts: string[];
  assumptions: string[];
  feelings: string[];
  needs: string[];
  draft: string;
  disclaimer: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const SYNTHETIC_EXAMPLE =
  "My housemate arrived after our agreed cooking time, and I felt frustrated.";

const sections: Array<{ key: keyof Pick<Reflection, "facts" | "assumptions" | "feelings" | "needs">; title: string; prompt: string }> = [
  { key: "facts", title: "Facts", prompt: "What can be observed without guessing intent?" },
  { key: "assumptions", title: "Assumptions", prompt: "What meaning might still need checking?" },
  { key: "feelings", title: "Feelings", prompt: "What is present for you?" },
  { key: "needs", title: "Needs", prompt: "What matters underneath the reaction?" },
];

export default function Home() {
  const [situation, setSituation] = useState("");
  const [reflection, setReflection] = useState<Reflection | null>(null);
  const [draft, setDraft] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("loading");
    setError("");
    setCopied(false);

    try {
      const response = await fetch(`${API_URL}/v1/reflections`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ situation }),
      });
      if (!response.ok) {
        const body = await response.json().catch(() => null);
        const message = body?.detail?.[0]?.msg;
        throw new Error(message ?? "Usmora could not reflect on that just now.");
      }
      const data = (await response.json()) as Reflection;
      setReflection(data);
      setDraft(data.draft);
      setStatus("idle");
    } catch (cause) {
      setStatus("error");
      setError(cause instanceof Error ? cause.message : "Usmora could not reflect on that just now.");
    }
  }

  async function copyDraft() {
    await navigator.clipboard.writeText(draft);
    setCopied(true);
  }

  return (
    <main>
      <header className="masthead">
        <a className="wordmark" href="#workspace" aria-label="Usmora home">
          Usmora<span aria-hidden="true">.</span>
        </a>
        <p>Pause · Reflect · Respond</p>
      </header>

      <section className="intro" aria-labelledby="page-title">
        <p className="eyebrow">A private communication pause</p>
        <h1 id="page-title">Untangle the moment before you reply.</h1>
        <p className="lede">
          Separate what happened from what you fear it means, notice what you need,
          and shape a message that still sounds like you.
        </p>
      </section>

      <section id="workspace" className="workspace" aria-label="Reflection workspace">
        <form className="reflection-form" onSubmit={submit}>
          <div className="form-heading">
            <div>
              <p className="step">01 · Describe</p>
              <h2>What happened?</h2>
              <p>Use a synthetic example in this prototype — not real relationship data.</p>
            </div>
            <button
              className="text-button"
              type="button"
              onClick={() => setSituation(SYNTHETIC_EXAMPLE)}
            >
              Use synthetic example
            </button>
          </div>
          <label htmlFor="situation">Describe the situation</label>
          <textarea
            id="situation"
            maxLength={4000}
            required
            rows={7}
            value={situation}
            onChange={(event) => setSituation(event.target.value)}
            placeholder="Keep to what happened, as if a camera recorded it…"
          />
          <div className="form-actions">
            <span>{situation.length} / 4000</span>
            <button className="primary-button" disabled={status === "loading"} type="submit">
              {status === "loading" ? "Reflecting…" : "Reflect on this"}
            </button>
          </div>
          {status === "error" && <p className="error" role="alert">{error}</p>}
        </form>

        {reflection && (
          <div className="result" aria-live="polite">
            <div className="result-heading">
              <p className="step">02 · Notice</p>
              <h2>A possible reading, not a verdict.</h2>
              <p>{reflection.disclaimer}</p>
            </div>
            <div className="reflection-grid">
              {sections.map((section) => (
                <article key={section.key} className="reflection-card">
                  <p>{section.prompt}</p>
                  <h3>{section.title}</h3>
                  <ul>
                    {reflection[section.key].map((item) => <li key={item}>{item}</li>)}
                  </ul>
                </article>
              ))}
            </div>
            <div className="draft-panel">
              <div>
                <p className="step">03 · Respond</p>
                <h2>Your draft, under your control.</h2>
                <p>Edit until it sounds like you. Usmora cannot send it.</p>
              </div>
              <label htmlFor="draft">Edit your message draft</label>
              <textarea
                id="draft"
                rows={7}
                value={draft}
                onChange={(event) => { setDraft(event.target.value); setCopied(false); }}
              />
              <div className="copy-row">
                <p role="status">{copied ? "Copied — you decide where it goes." : "Nothing leaves this page unless you copy it."}</p>
                <button className="secondary-button" type="button" onClick={copyDraft}>Copy draft</button>
              </div>
            </div>
          </div>
        )}
      </section>

      <aside className="trust" aria-label="Privacy and scope">
        <p>
          <strong>Private by design for this demo.</strong> Input is processed without persistence.
        </p>
        <p>
          Usmora is communication support — not therapy, diagnosis, emergency support,
          surveillance, or partner monitoring. Nothing is sent automatically.
        </p>
      </aside>
    </main>
  );
}

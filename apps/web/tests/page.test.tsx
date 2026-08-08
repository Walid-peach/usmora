import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import Home from "../app/page";

const reflection = {
  facts: ["A housemate arrived after an agreed cooking time."],
  assumptions: ["Their intention is not yet confirmed."],
  feelings: ["frustrated"],
  needs: ["reliability and shared expectations"],
  draft: "Hey, when dinner started late, I felt frustrated. Could we agree on updates?",
  disclaimer: "Prototype aid — review it as a perspective, not objective truth.",
};

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});


describe("Usmora reflection workspace", () => {
  it("shows the narrow workflow and trust boundaries", () => {
    render(<Home />);

    expect(screen.getByRole("heading", { name: /untangle the moment/i })).toBeVisible();
    expect(screen.getByText(/processed without persistence/i)).toBeVisible();
    expect(screen.getByText(/not therapy, diagnosis, emergency support/i)).toBeVisible();
    expect(screen.getByText(/nothing is sent automatically/i)).toBeVisible();
  });

  it("reflects, lets the user edit, and copies only on request", async () => {
    const user = userEvent.setup();
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => reflection,
    });
    const writeText = vi.fn().mockResolvedValue(undefined);
    vi.stubGlobal("fetch", fetchMock);
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText },
    });
    render(<Home />);

    const situation = screen.getByLabelText(/describe the situation/i);
    await user.type(situation, "A synthetic housemate dinner plan changed without an update.");
    await user.click(screen.getByRole("button", { name: /reflect on this/i }));

    expect(await screen.findByRole("heading", { name: "Facts" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "Assumptions" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "Feelings" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "Needs" })).toBeVisible();
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining("/v1/reflections"),
      expect.objectContaining({ method: "POST" }),
    );

    const draft = screen.getByLabelText(/edit your message draft/i);
    fireEvent.change(draft, { target: { value: "A calmer message I reviewed myself." } });
    await user.click(screen.getByRole("button", { name: /copy draft/i }));

    await waitFor(() => expect(writeText).toHaveBeenCalledWith("A calmer message I reviewed myself."));
    expect(screen.getByText(/copied — you decide where it goes/i)).toBeVisible();
  });

  it("shows a recoverable error without exposing the submitted situation", async () => {
    const user = userEvent.setup();
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("API unavailable")));
    render(<Home />);

    await user.type(screen.getByLabelText(/describe the situation/i), "Synthetic disagreement.");
    await user.click(screen.getByRole("button", { name: /reflect on this/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent("API unavailable");
    expect(screen.getByRole("button", { name: /reflect on this/i })).toBeEnabled();
  });
});

# aImL-HaCkAtHoN-iTech-
This was the repository created to submit the ai agent that has been created by the team code warriors for the Sairam Hackathon AIML and iTech .



````markdown
# TEAM CodeWarriors – Negotiation Agent Submission

## Overview
This repository contains the submission of **TEAM CodeWarriors** for the AI Negotiation Agent Competition.  
Our buyer agent, **"The Psychological Manipulator"**, is designed to dominate negotiations through **psychological pressure, authority projection, and time-based urgency**.  

The agent’s primary goal is to secure profitable deals while maintaining strict budget discipline and consistent character portrayal.

The project includes:
- A fully implemented negotiation agent in Python.
- Defined personality configuration for consistent manipulative behavior.
- A one-page strategy document explaining the agent’s approach.
- Requirements file for dependencies.

---

## Files Included
- `negotiation_agent_team_codewarriors.py` – Core implementation of the buyer agent.  
- `personality_config.json` – JSON definition of the agent’s manipulative traits, style, and catchphrases.  
- `STRATEGY.md` – Strategy explanation document (1 page).  
- `requirements.txt` – Dependencies list (Ollama + standard library).  
- `README.md` – Project documentation (this file).  

---

## How to Run
1. Ensure you are using **Python 3.8+**.  
2. Install dependencies using:  
   ```bash
   pip install -r requirements.txt
````

3. Run the negotiation test suite:

   ```bash
   python negotiation_agent_team_codewarriors.py
   ```

The script will simulate multiple negotiation rounds with a **mock seller** and print performance metrics (deal success, savings, and conversation log).

---

## Personality Summary

* **Name:** The Psychological Manipulator
* **Type:** Manipulative Strategist
* **Traits:** Confident, unpredictable, authoritative, pressuring, manipulative
* **Style:** Uses psychology and market logic to unsettle the seller. Anchors low, applies fear of loss, references alternative suppliers, and ramps up urgency in late rounds.
* **Catchphrases:**

  * "Market insiders are closing deals at lower rates."
  * "I have other suppliers lined up."
  * "We’re running out of time — this is my final serious offer."

---

## Competition Notes

* The agent is optimized to **never exceed budget**.
* **Early rounds:** Strict, aggressive countering below 90% of market price.
* **Late rounds:** More flexible, willing to accept up to 100% of market value if within budget.
* **Final round:** Always forces a deal to avoid timeout.
* Prioritizes **deal success rate**, **savings vs. market price**, and **character consistency**.

---

## Contributors

* **Team CodeWarriors** – AI Negotiation Agent Development & Strategy


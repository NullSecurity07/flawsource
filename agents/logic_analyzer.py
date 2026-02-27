from crewai import Agent

def create_logic_analyzer_agent(llm):
    return Agent(
        role='Principal Offensive Security Researcher',
        goal='Identify logical flaws, business logic errors, and deep security vulnerabilities based on the codebase map and exact API surfaces.',
        backstory=(
            "You are a top-tier cybersecurity researcher and white-hat hacker. "
            "You don't just look for missing brackets; you look for race "
            "conditions, broken access control, missing authorization checks "
            "on endpoints (which you receive from the regex tool), and "
            "flawed business logic. You think like an attacker."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

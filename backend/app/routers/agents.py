from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Agent, AgentRole
from app.schemas import AgentOut, AgentCreate
from app.services.registry_service import registry_adapter

router = APIRouter(prefix="/agents", tags=["Agents & Onchain Registry"])

@router.post("/register/", response_model=AgentOut, status_code=201)
@router.post("/register", response_model=AgentOut, status_code=201)
def register_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    """
    Registers a new buyer (store) or seller (farm) agent.
    Mints verifiable onchain identity on Solana Devnet via registry adapter.
    """
    agent = Agent(
        name=payload.name,
        role=payload.role,
        description=payload.description or "",
        latitude=payload.latitude,
        longitude=payload.longitude,
        zip_code=payload.zip_code,
        reputation_score=5.0
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)

    # Perform Solana onchain registration
    onchain_res = registry_adapter.register_agent(
        agent_id=agent.id,
        role=agent.role.value,
        name=agent.name
    )

    agent.solana_address = onchain_res.get("solana_address")
    agent.registry_tx = onchain_res.get("tx_signature")
    db.commit()
    db.refresh(agent)

    return agent

@router.get("/", response_model=list[AgentOut])
def list_agents(role: str = None, db: Session = Depends(get_db)):
    """Lists all registered agents, optionally filtered by role (buyer / seller)."""
    query = db.query(Agent)
    if role:
        query = query.filter(Agent.role == role)
    return query.all()

@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Fetches details for a single agent including Solana registry identity."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

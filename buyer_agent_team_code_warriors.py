"""
===========================================
AI NEGOTIATION AGENT - INTERVIEW TEMPLATE
===========================================

Buyer Agent: Psychological Manipulator (Improved with Flexible Acceptance)
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import random

# ============================================
# PART 1: DATA STRUCTURES (DO NOT MODIFY)
# ============================================

@dataclass
class Product:
    """Product being negotiated"""
    name: str
    category: str
    quantity: int
    quality_grade: str  # 'A', 'B', or 'Export'
    origin: str
    base_market_price: int  # Reference price for this product
    attributes: Dict[str, Any]

@dataclass
class NegotiationContext:
    """Current negotiation state"""
    product: Product
    your_budget: int  # Your maximum budget (NEVER exceed this)
    current_round: int
    seller_offers: List[int]  # History of seller's offers
    your_offers: List[int]  # History of your offers
    messages: List[Dict[str, str]]  # Full conversation history

class DealStatus(Enum):
    ONGOING = "ongoing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TIMEOUT = "timeout"


# ============================================
# PART 2: BASE AGENT CLASS (DO NOT MODIFY)
# ============================================

class BaseBuyerAgent(ABC):
    """Base class for all buyer agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.personality = self.define_personality()
        
    @abstractmethod
    def define_personality(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        pass
    
    @abstractmethod
    def respond_to_seller_offer(
        self, context: NegotiationContext, seller_price: int, seller_message: str
    ) -> Tuple[DealStatus, int, str]:
        pass
    
    @abstractmethod
    def get_personality_prompt(self) -> str:
        pass


# ============================================
# PART 3: YOUR BUYER AGENT
# ============================================

class YourBuyerAgent(BaseBuyerAgent):
    """
    Buyer Agent Personality: Psychological Manipulator
    Improved acceptance logic:
    - Strict early rounds
    - Flexible late rounds
    - Final fallback to avoid missed deals
    """

    def define_personality(self) -> Dict[str, Any]:
        return {
            "personality_type": "psychological_manipulator",
            "traits": ["confident", "unpredictable", "authoritative", "pressuring", "manipulative"],
            "negotiation_style": (
                "Uses psychology and market logic to unsettle the seller. "
                "Opens with strong anchoring, invokes insider knowledge, "
                "and applies pressure through doubt, scarcity, and time urgency. "
                "Adapts to seller concessions while keeping the upper hand."
            ),
            "catchphrases": [
                "Market insiders are closing deals at lower rates.",
                "I have other suppliers lined up.",
                "We’re running out of time — this is my final serious offer."
            ]
        }

    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        import ollama
        prompt = f"""
You are a buyer agent with the following personality:
{self.get_personality_prompt()}

You are negotiating for {context.product.name}, market price ₹{context.product.base_market_price}, 
quantity {context.product.quantity}, quality {context.product.quality_grade}.

Generate an opening offer that is manipulative yet within budget ₹{context.your_budget}. 
Tactics you may use: anchoring, invoking insider market knowledge, and psychological pressure.

Return only:
offer_amount: <number>
message: <2-3 sentence manipulative message including personality tone>
"""
        response = ollama.chat(
            model="llama3:8b",
            messages=[{"role": "user", "content": prompt}]
        )

        offer_amount = int(context.product.base_market_price * 0.8)  # fallback
        message = "Let's begin."
        text = str(response)

        match = re.search(r"offer_amount:\s*(\d+)", text)
        if match:
            offer_amount = min(int(match.group(1)), context.your_budget)
        match_msg = re.search(r"message:\s*(.+)", text, re.DOTALL)
        if match_msg:
            message = match_msg.group(1).strip()
        return offer_amount, message

    def respond_to_seller_offer(
        self, context: NegotiationContext, seller_price: int, seller_message: str
    ) -> Tuple[DealStatus, int, str]:
        import ollama
        prompt = f"""
You are a buyer agent with the following personality:
{self.get_personality_prompt()}

You are negotiating for {context.product.name}, market price ₹{context.product.base_market_price}, 
quantity {context.product.quantity}, quality {context.product.quality_grade}.
Current round: {context.current_round}
Seller offered ₹{seller_price} with message: "{seller_message}"
Previous buyer offers: {context.your_offers}

Respond strategically using manipulative tactics:
- Question the seller’s pricing logic
- Reference "other suppliers" or "insider knowledge"
- Apply time pressure if late rounds
- Be strict in early rounds, but more flexible in later rounds
- Only ACCEPT if seller’s price ≤ budget and:
    * ≤ 90% of market (early rounds)
    * ≤ 100% of market (late rounds ≥ 8)

Return only:
deal_status: <ACCEPTED or ONGOING>
counter_offer: <number>
message: <your manipulative response>
"""
        response = ollama.chat(
            model="llama3:8b",
            messages=[{"role": "user", "content": prompt}]
        )

        deal_status = DealStatus.ONGOING
        counter_offer = int(context.product.base_market_price * 0.9)
        message = "I’ll consider my next move."
        text = str(response)

        market_price = context.product.base_market_price

        # --- Acceptance logic (strict early, flexible late) ---
        if seller_price <= context.your_budget:
            if (context.current_round < 8 and seller_price <= market_price * 0.9) or \
               (context.current_round >= 8 and seller_price <= market_price):
                return DealStatus.ACCEPTED, seller_price, f"Deal accepted at ₹{seller_price}. You’re lucky I’m closing now."

        # --- Counter-offer extraction ---
        match_offer = re.search(r"counter_offer:\s*(\d+)", text)
        if match_offer:
            counter_offer = min(int(match_offer.group(1)), context.your_budget)

        match_msg = re.search(r"message:\s*(.+)", text, re.DOTALL)
        if match_msg:
            message = match_msg.group(1).strip()

        # --- Final fallback at round 10 ---
        if context.current_round >= 10 and seller_price <= context.your_budget:
            return DealStatus.ACCEPTED, seller_price, f"Fine, I’ll take ₹{seller_price}. Let’s close this now."

        return deal_status, counter_offer, message

    def get_personality_prompt(self) -> str:
        return (
            "I am a Psychological Manipulator negotiator. "
            "I use psychology, doubt, and pressure to dominate negotiations. "
            "I mix authority and insider knowledge with threats of walking away. "
            "I reference other suppliers and market insiders, and I apply time pressure in late rounds. "
            "Catchphrases include 'Market insiders are closing deals at lower rates.', "
            "'I have other suppliers lined up.', and "
            "'We’re running out of time — this is my final serious offer.'"
        )



# ============================================
# PART 5: TESTING FRAMEWORK (DO NOT MODIFY)
# ============================================

class MockSellerAgent:
    """A simple mock seller for testing your agent"""
    
    def __init__(self, min_price: int, personality: str = "standard"):
        self.min_price = min_price
        self.personality = personality
        
    def get_opening_price(self, product: Product) -> Tuple[int, str]:
        # Start at 150% of market price
        price = int(product.base_market_price * 1.5)
        return price, f"These are premium {product.quality_grade} grade {product.name}. I'm asking ₹{price}."
    
    def respond_to_buyer(self, buyer_offer: int, round_num: int) -> Tuple[int, str, bool]:
        if buyer_offer >= self.min_price * 1.1:  # Good profit
            return buyer_offer, f"You have a deal at ₹{buyer_offer}!", True
            
        if round_num >= 8:  # Close to timeout
            counter = max(self.min_price, int(buyer_offer * 1.05))
            return counter, f"Final offer: ₹{counter}. Take it or leave it.", False
        else:
            counter = max(self.min_price, int(buyer_offer * 1.15))
            return counter, f"I can come down to ₹{counter}.", False


def run_negotiation_test(buyer_agent: BaseBuyerAgent, product: Product, buyer_budget: int, seller_min: int) -> Dict[str, Any]:
    """Test a negotiation between your buyer and a mock seller"""
    
    seller = MockSellerAgent(seller_min)
    context = NegotiationContext(
        product=product,
        your_budget=buyer_budget,
        current_round=0,
        seller_offers=[],
        your_offers=[],
        messages=[]
    )
    
    # Seller opens
    seller_price, seller_msg = seller.get_opening_price(product)
    context.seller_offers.append(seller_price)
    context.messages.append({"role": "seller", "message": seller_msg})
    
    # Run negotiation
    deal_made = False
    final_price = None
    
    for round_num in range(10):  # Max 10 rounds
        context.current_round = round_num + 1
        
        # Buyer responds
        if round_num == 0:
            buyer_offer, buyer_msg = buyer_agent.generate_opening_offer(context)
            status = DealStatus.ONGOING
        else:
            status, buyer_offer, buyer_msg = buyer_agent.respond_to_seller_offer(
                context, seller_price, seller_msg
            )
        
        context.your_offers.append(buyer_offer)
        context.messages.append({"role": "buyer", "message": buyer_msg})
        
        if status == DealStatus.ACCEPTED:
            deal_made = True
            final_price = seller_price
            break
            
        # Seller responds
        seller_price, seller_msg, seller_accepts = seller.respond_to_buyer(buyer_offer, round_num)
        
        if seller_accepts:
            deal_made = True
            final_price = buyer_offer
            context.messages.append({"role": "seller", "message": seller_msg})
            break
            
        context.seller_offers.append(seller_price)
        context.messages.append({"role": "seller", "message": seller_msg})
    
    # Calculate results
    result = {
        "deal_made": deal_made,
        "final_price": final_price,
        "rounds": context.current_round,
        "savings": buyer_budget - final_price if deal_made else 0,
        "savings_pct": ((buyer_budget - final_price) / buyer_budget * 100) if deal_made else 0,
        "below_market_pct": ((product.base_market_price - final_price) / product.base_market_price * 100) if deal_made else 0,
        "conversation": context.messages
    }
    
    return result


# ============================================
# PART 6: TEST YOUR AGENT
# ============================================

def test_your_agent():
    """Run this to test your agent implementation"""
    
    # Create test products
    test_products = [
        Product(
            name="Alphonso Mangoes",
            category="Mangoes",
            quantity=100,
            quality_grade="A",
            origin="Ratnagiri",
            base_market_price=180000,
            attributes={"ripeness": "optimal", "export_grade": True}
        ),
        Product(
            name="Kesar Mangoes", 
            category="Mangoes",
            quantity=150,
            quality_grade="B",
            origin="Gujarat",
            base_market_price=150000,
            attributes={"ripeness": "semi-ripe", "export_grade": False}
        )
    ]
    
    # Initialize your agent
    your_agent = YourBuyerAgent("TestBuyer")
    
    print("="*60)
    print(f"TESTING YOUR AGENT: {your_agent.name}")
    print(f"Personality: {your_agent.personality['personality_type']}")
    print("="*60)
    
    total_savings = 0
    deals_made = 0
    
    # Run multiple test scenarios
    for product in test_products:
        for scenario in ["easy", "medium", "hard"]:
            if scenario == "easy":
                buyer_budget = int(product.base_market_price * 1.2)
                seller_min = int(product.base_market_price * 0.8)
            elif scenario == "medium":
                buyer_budget = int(product.base_market_price * 1.0)
                seller_min = int(product.base_market_price * 0.85)
            else:  # hard
                buyer_budget = int(product.base_market_price * 0.9)
                seller_min = int(product.base_market_price * 0.82)
            
            print(f"\nTest: {product.name} - {scenario} scenario")
            print(f"Your Budget: ₹{buyer_budget:,} | Market Price: ₹{product.base_market_price:,}")
            
            result = run_negotiation_test(your_agent, product, buyer_budget, seller_min)
            
            if result["deal_made"]:
                deals_made += 1
                total_savings += result["savings"]
                print(f"✅ DEAL at ₹{result['final_price']:,} in {result['rounds']} rounds")
                print(f"   Savings: ₹{result['savings']:,} ({result['savings_pct']:.1f}%)")
                print(f"   Below Market: {result['below_market_pct']:.1f}%")
            else:
                print(f"❌ NO DEAL after {result['rounds']} rounds")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print(f"Deals Completed: {deals_made}/6")
    print(f"Total Savings: ₹{total_savings:,}")
    print(f"Success Rate: {deals_made/6*100:.1f}%")
    print("="*60)


# ============================================
# PART 7: EVALUATION CRITERIA
# ============================================

"""
YOUR SUBMISSION WILL BE EVALUATED ON:

1. **Deal Success Rate (30%)**
   - How often you successfully close deals
   - Avoiding timeouts and failed negotiations

2. **Savings Achieved (30%)**
   - Average discount from seller's opening price
   - Performance relative to market price

3. **Character Consistency (20%)**
   - How well you maintain your chosen personality
   - Appropriate use of catchphrases and style

4. **Code Quality (20%)**
   - Clean, well-structured implementation
   - Good use of helper methods
   - Clear documentation

BONUS POINTS FOR:
- Creative, unique personalities
- Sophisticated negotiation strategies
- Excellent adaptation to different scenarios
"""

# ============================================
# PART 8: SUBMISSION CHECKLIST
# ============================================

"""
BEFORE SUBMITTING, ENSURE:

[ ] Your agent is fully implemented in YourBuyerAgent class
[ ] You've defined a clear, consistent personality
[ ] Your agent NEVER exceeds its budget
[ ] You've tested using test_your_agent()
[ ] You've added helpful comments explaining your strategy
[ ] You've included any additional helper methods

SUBMIT:
1. This completed template file
2. A 1-page document explaining:
   - Your chosen personality and why
   - Your negotiation strategy
   - Key insights from testing

FILENAME: negotiation_agent_[your_name].py
"""

if __name__ == "__main__":
    # Run this to test your implementation
    test_your_agent()
    
    # Uncomment to see how the example agent performs
    # print("\n\nTESTING EXAMPLE AGENT FOR COMPARISON:")
    # example_agent = ExampleSimpleAgent("ExampleBuyer")
    # test_your_agent()

import random
from datetime import datetime, time

# =========================
# Agent Lists
# =========================
onSiteItAgents = ["+441234567890", "+441234567891", "+441234567892"]
globalHelpDeskAgents = ["+441111111111", "+441111111112", "+441111111113"]
hrAgents = ["+442222222221", "+442222222222"]
facilitiesAgents = ["+443333333331", "+443333333332"]

# =========================
# Department Working Hours
# =========================
# Each department has different business hours
workingHours = {
    "IT":      (time(9, 0, 0),  time(17, 0, 0)),
    "HR":      (time(8, 30, 0), time(16, 30, 0)),
    "Facilities": (time(7, 0, 0),  time(15, 0, 0)),
}

# =========================
# Call Routing Mode
# =========================
# Options: "round_robin" or "call_all"
distributionMode = "round_robin"

# For round robin tracking
roundRobinIndex = {
    "IT_OnSite": 0,
    "IT_Global": 0,
    "HR": 0,
    "Facilities": 0
}

# =========================
# Helper Functions
# =========================

def getCallTime():
    """Ask the user for a call time and return as datetime."""
    while True:
        timeInput = input("Enter call time (HH:MM, 24-hour format): ").strip()
        try:
            callTimeObj = datetime.strptime(timeInput, "%H:%M")
            callTime = datetime.now().replace(
                hour=callTimeObj.hour,
                minute=callTimeObj.minute,
                second=0,
                microsecond=0
            )
            return callTime
        except ValueError:
            print("Invalid format. Please use HH:MM (e.g., 14:30).")


def getMenuChoice():
    """Display IVR menu and get user choice."""
    print("\n--- IVR MENU ---")
    print("Press 1 for IT Support")
    print("Press 2 for HR")
    print("Press 3 for Facilities\n")

    while True:
        choice = input("Enter your choice: ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print("Invalid choice. Please select 1, 2, or 3.")


def isWithinHours(callTime, deptName):
    """Check if call is within working hours for a department."""
    start, end = workingHours[deptName]
    return start <= callTime.time() <= end


def selectAgent(agentList, deptKey):
    """Choose agent based on distribution mode."""
    global roundRobinIndex

    if distributionMode == "round_robin":
        # Round robin selection
        idx = roundRobinIndex[deptKey] % len(agentList)
        agent = agentList[idx]
        roundRobinIndex[deptKey] += 1
        print(f"   -> [Round Robin] Assigning agent at index {idx}")
        return agent

    elif distributionMode == "call_all":
        # All agents ring at once (simulate one picking up)
        print(f"   -> [Call All] All agents ringing: {', '.join(agentList)}")
        agent = random.choice(agentList)
        print(f"   -> First to answer: {agent}")
        return agent


def getItAgent(callTime):
    """Route IT calls based on business hours."""
    print(f" Step 3: Checking IT working hours {workingHours['IT']}...")
    if isWithinHours(callTime, "IT"):
        print("  -> Within IT business hours, routing to On-Site IT Support")
        return "On-Site IT Support", selectAgent(onSiteItAgents, "IT_OnSite")
    else:
        print("  -> Outside IT business hours, routing to Global Help Desk")
        return "Global Help Desk", selectAgent(globalHelpDeskAgents, "IT_Global")


def getHrAgent(callTime):
    """Route HR calls based on business hours."""
    print(f" Step 3: Checking HR working hours {workingHours['HR']}...")
    if isWithinHours(callTime, "HR"):
        print("  -> Within HR hours, routing to HR Department")
        return "HR Department", selectAgent(hrAgents, "HR")
    else:
        print("  -> Outside HR hours, no agents available")
        return "HR Department (Voicemail)", None


def getFacilitiesAgent(callTime):
    """Route Facilities calls based on business hours."""
    print(f" Step 3: Checking Facilities working hours {workingHours['Facilities']}...")
    if isWithinHours(callTime, "Facilities"):
        print("  -> Within Facilities hours, routing to Facilities Team")
        return "Facilities Team", selectAgent(facilitiesAgents, "Facilities")
    else:
        print("  -> Outside Facilities hours, no agents available")
        return "Facilities (Voicemail)", None


def routeCall(departmentChoice, callTime):
    """Route call based on department and time."""
    print(f" Step 2: Caller selected option {departmentChoice}")

    if departmentChoice == "1":
        return getItAgent(callTime)
    elif departmentChoice == "2":
        return getHrAgent(callTime)
    elif departmentChoice == "3":
        return getFacilitiesAgent(callTime)


def processCall():
    """Main process for handling a call."""
    callTime = getCallTime()
    print(f"\nStep 1: Incoming call registered at {callTime.strftime('%Y-%m-%d %H:%M:%S')}")

    departmentChoice = getMenuChoice()
    destination, agent = routeCall(departmentChoice, callTime)

    print("\nStep 4: Final result...")
    print(f"  -> Destination: {destination}")
    if agent:
        print(f"  -> Assigned agent number: {agent}")
    else:
        print("  -> No agents available at this time.")
    print("-" * 50)


if __name__ == "__main__":
    while True:
        processCall()
        again = input("\nWould you like to simulate another call? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting IVR simulation. Goodbye!")
            break

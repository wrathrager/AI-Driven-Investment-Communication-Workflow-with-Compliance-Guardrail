# AI-Driven-Investment-Communication-Workflow-with-Compliance-Guardrail
Built an AI-powered workflow that: 1. Reads scheduled investor communication data from a Google Sheet. 2. Validates inputs. 3. Applies a compliance guardrail layer before sending. 4. Sends approved messages at scheduled times.
Step 1: Input Source – Google Sheet
The Google Sheet contains the following columns:
● Name, mobile, message, schedule, category, status,
compliance_flag
● Create and use a google sheet with mentioned columns, populate with sample data
for testing.

1.1 Column Definitions
Name : Recipient name
Mobile : Recipient mobile number (string). Must pass format validation.
Message: Message to be sent.
Schedule: Datetime format: YYYY-MM-DD HH:MM (24-hour format)
Category : Message category

● Performance Update / Research Insight / Product Communication / Marketing
Status: System-updated field
● Pending / Scheduled / Sent / Failed / Invalid / Blocked
Compliance_flag: System-updated field
● Approved / Requires Review / Rejected

Step 2: Functional Workflow Layers

2.1 Data Reading Layer
The system must:
1. Read rows where:
○ status = empty OR
○ status = Pending
2. Process each row independently.

2.2 Validation Layer
Before any AI call:
Validate:
1. Mobile number format
2. Non-empty message
3. Valid datetime format
4. Schedule is not in the past
5. Category is one of allowed values

Step 3: Compliance Guardrail Layer
3.1 Purpose
Before sending any message, the system must check for:
● Performance claims without disclaimers
● Misleading language
● Investment advice without qualification
● Over-promising returns
● Words like:
○ “Guaranteed”
○ “Assured returns”
○ “Risk-free”
○ “Double your money”

3.2 AI Usage Requirements
You must use an Assistant / LLM API call to:
1. Classify message as:
○ Approved
○ Requires Review
○ Rejected
Important Constraints:
● LLM must NOT modify message.
● LLM must only classify.

3.3 Compliance Rules
After LLM classification:
If:
● Approved → proceed
● Requires Review → status = Blocked
● Rejected → status = Blocked
Blocked messages must not be scheduled or sent.

Step 4: Scheduling Layer
For rows where:
● compliance_flag = Approved
● validation passed
System must:
1. Schedule dispatch according to schedule column.
2. Prevent duplicate sending.
3. Update status to Scheduled.

Step 5: Sending Layer
At scheduled time:
1. Send message (Email or SMS/ WhatsApp API acceptable).
2. If success → status = Sent
3. If failure → status = Failed

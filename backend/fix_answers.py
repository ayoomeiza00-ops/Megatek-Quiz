import json

# The answer key you pasted, as a multiline string
ANSWER_TEXT = """
MEGATEK ICT ACADEMY
ICT QUIZ COMPETITION
150 Advanced Objective Questions — 15 Topic Sections
Official Answer Key for the 150 Quiz Competition Questions — for the quizmaster's use.

Instructions
• This document contains the correct answers for all 150 quiz competition questions.
• Answers are grouped under the same 15 sections as the question paper.
• Intended for the quizmaster or scorer — keep this key away from contestants during the competition.

SECTION 1: INTRODUCTION TO COMPUTERS & TECHNOLOGY

Q#	Correct Answer
1	B) getting fatigued
2	B) process data and follow a set of instructions
3	B) very short
4	B) accuracy
5	B) carry out
6	B) make repetitive and complex tasks faster and more accurate
7	B) proper electricity, ventilation, and safety arrangements
8	B) body strain and poor eyesight
9	B) accurately store and manage patient records and treatment schedules
10	A) accurately calculate, store, and track large amounts of money and transactions

SECTION 2: TYPES OF COMPUTERS

Q#	Correct Answer
11	B) portability
12	A) has a touch screen and no fixed physical keyboard
13	B) large organizations and companies
14	B) Smartphone, Laptop, Desktop
15	B) process data, run apps, and connect to the internet
16	A) have better cooling and can house larger components
17	B) travel and work from different locations
18	C) Mainframe computer
19	B) store files, browse the internet, and run many types of programs
20	A) can be adapted to perform many different useful tasks

SECTION 3: COMPUTER HARDWARE (PARTS OF THE COMPUTER)

Q#	Correct Answer
21	B) processing instructions and controlling operations
22	C) Monitor
23	B) display the results processed by the system unit
24	A) the keyboard enters text and commands, while the mouse selects and navigates
25	B) connection point where devices like a mouse or flash drive can be plugged in
26	B) CPU, which could overheat
27	A) processes information and makes decisions, similar to how the brain thinks
28	B) Typing and saving a document without being able to see it
29	B) Monitor – displays visual output
30	B) houses and connects the main components that make the computer function

SECTION 4: INPUT DEVICES

Q#	Correct Answer
31	B) allow users to send data and commands into the computer for processing
32	B) convert physical images into digital data for the computer
33	B) using a microphone with voice recognition software
34	B) scanner
35	A) lets us type letters and numbers directly
36	B) input
37	B) sends directional and control signals into the computer
38	A) sends sound into the computer, while a speaker sends sound out
39	B) reads and sends product information into the computer system
40	B) Input devices can be wired or wireless, as long as they send data into the computer

SECTION 5: OUTPUT DEVICES

Q#	Correct Answer
41	B) data goes in (input), is processed, and the result comes out (output)
42	B) displays processed information for others to see
43	B) Braille display or speech/audio output
44	A) allows the school to keep permanent paper copies of work, unlike a monitor
45	B) processed
46	A) visual and audio
47	A) check for mistakes before producing a paper copy
48	B) humans can see, hear, or use
49	A) sends processed information out of the computer onto paper
50	B) allow private listening without disturbing others

SECTION 6: THE KEYBOARD

Q#	Correct Answer
51	A) Backspace removes characters to the left, while Delete removes characters to the right of the cursor
52	A) lowercase
53	A) is pressed most frequently, to separate words while typing
54	B) Starting a new line and confirming a command or selection
55	B) Caps Lock is turned on
56	B) Shift
57	B) number keys type digits; arrow keys move the cursor around the screen
58	B) turn off Caps Lock and correct the affected text
59	B) performing special shortcut tasks, which vary by program
60	B) increases speed and accuracy over time through familiarity with key positions

SECTION 7: THE MOUSE

Q#	Correct Answer
61	A) shortcut menu with more options
62	A) allow a user to move or rearrange items by holding and moving the mouse
63	A) a single click selects an item; a double click typically opens it
64	B) move up and down a page without using the scroll bar directly
65	B) whether its batteries are low or it is properly connected
66	A) a light sensor
67	A) prevents hand strain and allows for smoother, more controlled movement
68	B) drag-and-drop
69	A) open a shortcut/context menu of options for a selected item
70	A) generally offers more precise and controlled pointer movement

SECTION 8: COMPUTER SOFTWARE

Q#	Correct Answer
71	A) hardware provides the physical parts, while software provides instructions that make the hardware perform useful tasks
72	B) manages the computer's overall resources and allows other programs to run
73	A) Windows – System Software; MS Word – Application Software
74	B) detecting, blocking, and removing harmful programs
75	A) the Operating System manages hardware and allows other software to run
76	B) application
77	A) can be used without payment, while paid software requires purchase or a license
78	B) the whole computer may become unusable until the issue is fixed
79	A) can fix errors and protect against newly discovered security threats
80	B) is a program used by the user to perform a specific task — browsing the internet

SECTION 9: STORAGE DEVICES & MEMORY

Q#	Correct Answer
81	A) RAM stores data temporarily while the computer is on; a hard disk stores data permanently
82	B) the unsaved essay is lost because it was only held in RAM
83	B) Floppy Disk, Flash Drive, Hard Disk
84	B) has very limited storage capacity and is fragile compared to modern options
85	B) usually holds permanent instructions that are not easily changed and are not lost when powered off
86	A) primary storage handles data currently in use for fast processing, while secondary storage keeps data permanently
87	B) external, removable
88	B) allows files to be saved and accessed remotely over the internet, without carrying a physical device
89	B) back up important files in case the computer's hard disk fails
90	A) prevent data corruption or loss from an incomplete file transfer

SECTION 10: THE INTERNET & WEB BROWSERS

Q#	Correct Answer
91	B) the Internet is the physical network connecting computers, while the WWW is a system of linked web pages accessed through it
92	B) finding relevant information or websites based on typed keywords
93	B) the unique address used to locate a specific resource or page on the internet
94	A) allows wireless, flexible access without needing cables to every device
95	B) sending an email to a friend
96	B) government organization
97	A) a single incorrect character can lead to an entirely different or unintended website
98	B) contain viruses or malicious software
99	A) a browser is software used to access websites; a search engine is a tool used to find information
100	B) users can choose based on speed, features, or compatibility with certain websites

SECTION 11: WORD PROCESSING

Q#	Correct Answer
101	A) lets you create a new file or change its name/location, while Save updates the current file
102	B) Bold
103	B) reverse the most recent action or change made
104	B) Print Preview
105	A) organize information logically, guiding the reader through the content
106	A) the paragraph was never actually copied/selected correctly first
107	A) type the title, then select it, then apply bold, centering, and font size changes
108	A) helps identify and correct possible spelling errors before printing or submitting
109	B) help users quickly find related tools/commands based on category
110	A) the title bar usually displays the current file name of the open document

SECTION 12: SPREADSHEETS

Q#	Correct Answer
111	A) tells Excel that what follows is a calculation, not just text
112	A) =A1+A2
113	A) organized data entry, quick calculations, and easy updates
114	A) visually represent data, making trends and comparisons easier to understand
115	A) =SUM(B2:B6)
116	A) allows formulas and functions to refer to exact locations for accurate calculations
117	B) there is a problem with how the formula or data was entered
118	B) calculates the mean (typical value) of a selected range of numbers
119	A) automatically calculate totals and help spot patterns more easily
120	A) rely on correctly referencing specific cells within the row-and-column grid

SECTION 13: COMPUTER LABORATORY CARE & SAFETY

Q#	Correct Answer
121	A) spills could damage sensitive electronic components and cause permanent faults
122	B) corrupt system files or cause loss of unsaved work
123	A) gives users a short time to save work and shut down safely during a power outage
124	A) prevent people from tripping and to avoid damaging the cables
125	B) wipe gently with a soft, dry microfiber cloth
126	A) could cause accidents and damage to expensive, sensitive equipment
127	B) cause overheating and reduce performance or damage components
128	A) damage sensitive electronic components or cause short circuits
129	A) keep the systems running safely, securely, and efficiently for all users
130	A) sitting too close for long periods can cause eye strain and discomfort over time

SECTION 14: INTERNET SAFETY & NETIQUETTE

Q#	Correct Answer
131	C) Bl6e#Sky92!
132	A) if one account is hacked, all other accounts using that password could also become vulnerable
133	B) refuse to share it and tell a trusted adult
134	B) a trick used by criminals to steal personal information through fake messages or links
135	A) once shared, content can be difficult to fully remove and may be seen by unintended people
136	B) repeatedly sending mean or threatening messages to someone online
137	A) these are common warning signs of an unsafe or untrustworthy website
138	B) the trail of data and activity a person leaves behind while using the internet
139	B) stop, avoid opening the download, and tell a trusted adult immediately
140	A) help protect children from content or interactions that may not be appropriate for their age

SECTION 15: EMERGING TECHNOLOGY (AI, CODING & NETWORKING)

Q#	Correct Answer
141	B) learn patterns and make decisions based on data, beyond fixed calculations
142	B) within a small area, such as a single school or office building
143	A) the Internet is an example of a very large WAN connecting networks worldwide
144	A) allow an action to repeat automatically without rewriting the same blocks multiple times
145	B) finding and correcting errors so a program works as intended
146	B) make a decision and trigger an action only when a certain condition is true
147	A) whoever follows it, human or computer, can achieve the correct result without confusion
148	A) store and access files from anywhere with an internet connection
149	A) a variable's value can change during a program, while a constant's value stays fixed
150	B) understand spoken language and respond appropriately to requests
"""

def extract_answer_map(text):
    """Parse the answer text and return a dict {question_number: correct_letter (A-D)}"""
    answer_map = {}
    lines = text.splitlines()
    for line in lines:
        # Look for lines that start with a number, then whitespace, then a letter A-D
        import re
        match = re.search(r'^(\d+)\s+([A-D])\)', line.strip())
        if match:
            q_num = int(match.group(1))
            letter = match.group(2)
            answer_map[q_num] = letter
    return answer_map

if __name__ == "__main__":
    # Load existing questions.json
    with open('questions.json', 'r') as f:
        questions = json.load(f)

    # Get answer map
    answer_map = extract_answer_map(ANSWER_TEXT)
    print(f"Found answers for {len(answer_map)} questions.")

    # Update each question
    for q in questions:
        q_id = q['id']
        if q_id in answer_map:
            letter = answer_map[q_id]
            # Convert letter to index: A->0, B->1, C->2, D->3
            q['correct'] = ord(letter) - 65
        else:
            print(f"⚠️ Warning: No answer for question {q_id}")

    # Write back
    with open('questions.json', 'w') as f:
        json.dump(questions, f, indent=2)

    print("✅ questions.json updated with correct answers.")
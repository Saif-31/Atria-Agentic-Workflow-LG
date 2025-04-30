import streamlit as st
from langchain_core.messages import AIMessage

from apple import (
    initialize_state, 
    classify_user_choice, 
    IntegratedState, 
    qa_agent_node, 
    process_user_input, 
    intelligent_agent_node, 
    reflection_agent_node, 
    classification_tool_node, 
    question_answer_manager_node,
    find_answer_in_history
)

# Add sidebar with New Chat button and User Guide
with st.sidebar:
    if st.button("New Chat", type="primary", use_container_width=True):
        # Reset the session state
        st.session_state.state = initialize_state()
        st.session_state.messages = []
        st.session_state.conversation_started = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### User Guide")
    
    with st.expander("How to Use Q&A Mode"):
        st.markdown("""
        **Questions & Answers Mode:**
        1. Click "Questions Answers" button
        2. Answer each question provided by the chatbot
        3. Type your responses in the chat input
        4. Wait for the next question
        5. Continue until all questions are answered
        6. View summary when complete
        """)
    
    with st.expander("How to Use Meeting Notes Mode"):
        st.markdown("""
        **Meeting Notes Analysis:**
        1. Click "Meeting Notes" button
        2. Paste your meeting notes in the text area
        3. Click "Submit Notes" to start analysis
        4. System will:
           - Analyze notes content
           - Generate relevant questions
           - Refine questions automatically
           - Identify unanswered topics
        5. Answer additional questions if needed
        6. Review final Q&A summary
        """)
    
    with st.expander("Tips & Features"):
        st.markdown("""
        **Helpful Tips:**
        - Use "New Chat" to start over
        - Provide detailed responses
        - Wait for processing between steps
        - Review summaries carefully
        - All data is processed securely
        """)

st.title("Atria's AI Agentic System")

# Initialize the state if it doesn't exist
if 'state' not in st.session_state:
    st.session_state.state = initialize_state()

# Initialize message history in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display greeting and options
st.markdown("#### Welcome to the Meeting Chatbot!")
st.markdown("---")
st.markdown("##### Would you like to start with:")
st.markdown("")

# Create columns for the buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("1. Questions Answers", type="primary"):
        choice = classify_user_choice("1")
        st.session_state.state["mode"] = choice
        st.session_state.state["current_phase"] = "qa_phase"
        st.session_state.state["status"] = "Starting Q&A session"
        # Initialize conversation state
        st.session_state.conversation_started = False
        st.session_state.state["conversation_history"] = []
        st.rerun()

with col2:
    if st.button("2. Meeting Notes", type="primary"):
        choice = classify_user_choice("2")
        st.session_state.state["mode"] = choice
        st.session_state.state["current_phase"] = "qa_phase"
        st.session_state.state["status"] = "Processing meeting notes"
        # Initialize notes in session state
        st.session_state.state["notes"] = ""
        st.rerun()

# Display current status and handle different modes
if st.session_state.state.get("mode"):
    st.write(f"Status: {st.session_state.state['status']}")
    
    if st.session_state.state["mode"] == "q_and_a":
        # Create a container for the chat
        chat_container = st.container()
        
        with chat_container:
            # Start conversation if not started
            if not st.session_state.get("conversation_started", False):
                with st.spinner("Starting conversation..."):
                    updated_state = qa_agent_node(st.session_state.state)
                    st.session_state.state = updated_state
                    st.session_state.conversation_started = True
                    st.rerun()
            
            # Create chat message area
            st.markdown("### Meeting Assistant Chat")
            chat_area = st.container()
            
            with chat_area:
                # Get conversation history and current question
                history = st.session_state.state.get("conversation_history", [])
                current_question = st.session_state.state.get("current_question")
                
                # Display all messages from history
                for message in history:
                    role = "assistant" if isinstance(message, AIMessage) else "user"
                    with st.chat_message(role):
                        st.markdown(message.content)
                
                # Only display current question if it's not already in history
                if (current_question and 
                    not st.session_state.state.get("interview_completed", False) and 
                    not any(msg.content == current_question for msg in history if isinstance(msg, AIMessage))):
                    with st.chat_message("assistant"):
                        st.markdown(current_question)
                
                # User input area
                if not st.session_state.state.get("interview_completed", False):
                    if user_response := st.chat_input("Your response..."):
                        with st.chat_message("user"):
                            st.markdown(user_response)
                        
                        with st.spinner("Processing your response..."):
                            updated_state = process_user_input(st.session_state.state, user_response)
                            st.session_state.state = updated_state
                            st.rerun()
                else:
                    st.success("Interview completed! Thank you for your responses.")
                    if st.button("View Summary", type="primary"):
                        st.markdown("### Meeting Summary")
                        st.json(st.session_state.state.get("meeting_details", {}))

    elif st.session_state.state["mode"] == "meeting_notes":
        if not st.session_state.state.get("notes_processed", False):
            st.markdown("### Please enter your meeting notes below:")
            notes = st.text_area("Meeting Notes", height=300)
            
            if st.button("Submit Notes", type="primary"):
                if notes.strip():
                    # Phase 1: Process with qa_agent_node
                    with st.spinner("Analyzing meeting notes..."):
                        st.session_state.state["notes"] = notes
                        updated_state = qa_agent_node(st.session_state.state)
                        st.session_state.state = updated_state
                        st.session_state.state["notes_processed"] = True
                        st.success("Notes Analysis Complete!")
                        
                        # Process with intelligent agent
                        st.info("Starting Question Generation...")
                        with st.spinner("Generating questions from notes..."):
                            st.session_state.state["intelligent_conversation_history"] = [
                                {"role": "assistant", "content": st.session_state.state.get("meeting_details", {}).get("extracted_from_notes", "")}
                            ]
                            updated_state = intelligent_agent_node(st.session_state.state)
                            st.session_state.state = updated_state
                            
                        # Process with reflection agent
                        st.info("Refining Generated Questions...")
                        with st.spinner("Improving question quality..."):
                            updated_state = reflection_agent_node(st.session_state.state)
                            st.session_state.state = updated_state
                            
                        # Process with classification
                        st.info("Classifying Questions...")
                        with st.spinner("Identifying unanswered questions..."):
                            updated_state = classification_tool_node(st.session_state.state)
                            st.session_state.state = updated_state
                            
                            # Display only unanswered questions
                            st.markdown("### Questions Needing Answers")
                            unanswered = st.session_state.state.get("classified_unanswered_questions", [])
                            for i, q in enumerate(unanswered, 1):
                                st.markdown(f"{i}. {q}")
                            
                            if unanswered:
                                st.session_state.state["questions_need_answers"] = True
                            
                        st.rerun()
                else:
                    st.error("Please enter some notes before submitting.")
        
        else:
            # After classification
            if not st.session_state.state.get("qa_completed", False):
                unanswered = st.session_state.state.get("classified_unanswered_questions", [])
                
                if "current_qa_index" not in st.session_state:
                    st.session_state.current_qa_index = 0
                    st.session_state.answers = {}
                
                if st.session_state.current_qa_index < len(unanswered):
                    # Display current question
                    current_q = unanswered[st.session_state.current_qa_index]
                    st.info("Please answer the following question:")
                    st.markdown(f"**Q{st.session_state.current_qa_index + 1}:** {current_q}")
                    
                    # Get user's answer
                    answer = st.text_area("Your answer:", key=f"answer_{st.session_state.current_qa_index}")
                    
                    if st.button("Submit Answer", type="primary"):
                        if answer.strip():
                            # Store answer
                            st.session_state.answers[current_q] = answer
                            st.session_state.current_qa_index += 1
                            st.rerun()
                        else:
                            st.error("Please provide an answer before proceeding.")
                else:
                    # All questions answered, prepare final list
                    all_qa_pairs = []
                    
                    # Add previously answered questions
                    for q in st.session_state.state.get("classified_answered_questions", []):
                        answer = find_answer_in_history(q, st.session_state.state["conversation_history"])
                        all_qa_pairs.append({"question": q, "answer": answer or "Found in meeting notes"})
                    
                    # Add newly answered questions
                    for q, a in st.session_state.answers.items():
                        all_qa_pairs.append({"question": q, "answer": a})
                    
                    # Display complete Q&A list
                    st.success("All questions have been answered!")
                    st.markdown("### Complete Questions & Answers")
                    
                    for i, qa in enumerate(all_qa_pairs, 1):
                        st.markdown(f"**Q{i}:** {qa['question']}")
                        st.markdown(f"**A:** {qa['answer']}")
                        st.markdown("---")
                    
                    st.session_state.qa_completed = True




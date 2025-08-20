"""
UI Enhancements Module
Adds cancel buttons and improves user experience with abort capabilities
"""
import streamlit as st
from datetime import datetime

def add_cancel_button(form_key, cancel_action=None):
    """Add a standardized cancel button to forms"""
    if st.button("❌ Cancel", key=f"cancel_{form_key}", use_container_width=True):
        if cancel_action:
            cancel_action()
        else:
            # Default action: clear form state
            if f"{form_key}_active" in st.session_state:
                st.session_state[f"{form_key}_active"] = False
            st.rerun()
    return False

def confirmation_dialog(message, confirm_text="Confirm", cancel_text="Cancel"):
    """Show a confirmation dialog with cancel option"""
    col1, col2 = st.columns(2)
    
    with col1:
        confirm = st.button(f"✅ {confirm_text}", use_container_width=True)
    
    with col2:
        cancel = st.button(f"❌ {cancel_text}", use_container_width=True)
    
    if cancel:
        return False
    
    return confirm

def process_with_cancel(process_name, steps, allow_cancel=True):
    """Execute a multi-step process with cancel capability"""
    
    # Initialize progress tracking
    if f"{process_name}_active" not in st.session_state:
        st.session_state[f"{process_name}_active"] = False
        st.session_state[f"{process_name}_step"] = 0
    
    if not st.session_state[f"{process_name}_active"]:
        return None
    
    progress_container = st.container()
    
    with progress_container:
        # Show progress bar
        current_step = st.session_state[f"{process_name}_step"]
        progress = current_step / len(steps)
        st.progress(progress)
        st.write(f"Step {current_step + 1} of {len(steps)}: {steps[current_step]['name']}")
        
        # Cancel button
        if allow_cancel:
            if st.button("🛑 Cancel Process", key=f"cancel_process_{process_name}"):
                st.session_state[f"{process_name}_active"] = False
                st.session_state[f"{process_name}_step"] = 0
                st.warning(f"Process '{process_name}' cancelled")
                st.rerun()
        
        # Execute current step
        try:
            result = steps[current_step]['function']()
            
            # Move to next step
            st.session_state[f"{process_name}_step"] += 1
            
            if st.session_state[f"{process_name}_step"] >= len(steps):
                # Process complete
                st.session_state[f"{process_name}_active"] = False
                st.session_state[f"{process_name}_step"] = 0
                st.success(f"Process '{process_name}' completed successfully!")
                return "completed"
            else:
                st.rerun()
                
        except Exception as e:
            st.error(f"Error in step {current_step + 1}: {str(e)}")
            if st.button("Retry", key=f"retry_{process_name}_{current_step}"):
                st.rerun()
            if st.button("Skip Step", key=f"skip_{process_name}_{current_step}"):
                st.session_state[f"{process_name}_step"] += 1
                st.rerun()
            if st.button("Cancel Process", key=f"abort_{process_name}_{current_step}"):
                st.session_state[f"{process_name}_active"] = False
                st.session_state[f"{process_name}_step"] = 0
                st.rerun()

def auto_save_form(form_key, data, interval_seconds=30):
    """Auto-save form data with ability to restore"""
    
    # Save current state
    if f"{form_key}_last_save" not in st.session_state:
        st.session_state[f"{form_key}_last_save"] = datetime.now()
        st.session_state[f"{form_key}_data"] = data
    
    # Check if auto-save needed
    time_since_save = (datetime.now() - st.session_state[f"{form_key}_last_save"]).seconds
    
    if time_since_save >= interval_seconds:
        st.session_state[f"{form_key}_data"] = data
        st.session_state[f"{form_key}_last_save"] = datetime.now()
        st.success("✅ Auto-saved", icon="💾")
    
    # Restore option
    if st.button("↩️ Restore Last Save", key=f"restore_{form_key}"):
        return st.session_state.get(f"{form_key}_data", {})
    
    return None

def undo_manager(action_key, max_history=10):
    """Manage undo/redo functionality"""
    
    if f"{action_key}_history" not in st.session_state:
        st.session_state[f"{action_key}_history"] = []
        st.session_state[f"{action_key}_index"] = -1
    
    col1, col2, col3 = st.columns([1, 1, 8])
    
    with col1:
        if st.button("↩️ Undo", key=f"undo_{action_key}", 
                    disabled=st.session_state[f"{action_key}_index"] < 0):
            if st.session_state[f"{action_key}_index"] >= 0:
                st.session_state[f"{action_key}_index"] -= 1
                return "undo"
    
    with col2:
        if st.button("↪️ Redo", key=f"redo_{action_key}",
                    disabled=st.session_state[f"{action_key}_index"] >= len(st.session_state[f"{action_key}_history"]) - 1):
            if st.session_state[f"{action_key}_index"] < len(st.session_state[f"{action_key}_history"]) - 1:
                st.session_state[f"{action_key}_index"] += 1
                return "redo"
    
    return None

def add_action_to_history(action_key, action_data):
    """Add an action to the undo history"""
    if f"{action_key}_history" not in st.session_state:
        st.session_state[f"{action_key}_history"] = []
        st.session_state[f"{action_key}_index"] = -1
    
    # Remove any actions after current index (for new branch)
    st.session_state[f"{action_key}_history"] = st.session_state[f"{action_key}_history"][:st.session_state[f"{action_key}_index"] + 1]
    
    # Add new action
    st.session_state[f"{action_key}_history"].append(action_data)
    st.session_state[f"{action_key}_index"] = len(st.session_state[f"{action_key}_history"]) - 1
    
    # Limit history size
    max_history = 10
    if len(st.session_state[f"{action_key}_history"]) > max_history:
        st.session_state[f"{action_key}_history"] = st.session_state[f"{action_key}_history"][-max_history:]
        st.session_state[f"{action_key}_index"] = len(st.session_state[f"{action_key}_history"]) - 1

def get_current_action(action_key):
    """Get the current action from history"""
    if f"{action_key}_history" in st.session_state and st.session_state[f"{action_key}_index"] >= 0:
        return st.session_state[f"{action_key}_history"][st.session_state[f"{action_key}_index"]]
    return None
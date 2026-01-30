
import base64
import json
import time
import streamlit as st
import requests
import uuid

# Configuration
BACKEND_URL = "http://localhost:8001/chat"
SESSIONS_URL = "http://localhost:8001/sessions"
LOGIN_URL = "http://localhost:8001/auth/login"
REGISTER_URL = "http://localhost:8001/auth/register"
REFRESH_URL = "http://localhost:8001/auth/refresh"
st.set_page_config(page_title="ADK Chatbot", page_icon="🤖")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "auth_token" not in st.session_state:
    st.session_state.auth_token = None


def _jwt_expiry(token: str):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        padding = "=" * (-len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload + padding)
        data = json.loads(decoded.decode("utf-8"))
        return data.get("exp")
    except Exception:
        return None


def safe_request(method, url, **kwargs):
    try:
        resp = requests.request(method, url, **kwargs)
        if resp.status_code == 401 and st.session_state.auth_token:
            headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
            refresh = requests.post(REFRESH_URL, headers=headers, timeout=10)
            if refresh.status_code == 200:
                st.session_state.auth_token = refresh.json().get("access_token")
                headers = kwargs.get("headers", {})
                headers["Authorization"] = f"Bearer {st.session_state.auth_token}"
                kwargs["headers"] = headers
                return requests.request(method, url, **kwargs)
            st.error("Session expired, please log in again.")
        return resp
    except Exception:
        return None

# UI Layout
st.title("🤖 Google ADK Chatbot")
st.caption("Powered by Deepmind Agentic Coding")

# Auth Sidebar
with st.sidebar:
    st.header("Account")
    if not st.session_state.auth_token:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                resp = requests.post(LOGIN_URL, json={"email": email, "password": password}, timeout=15)
                if resp.status_code == 200:
                    st.session_state.auth_token = resp.json().get("access_token")
                    st.success("Logged in")
                else:
                    st.error(resp.text)
            except Exception as exc:
                st.error(f"Login failed: {exc}")
        if st.button("Register"):
            try:
                resp = requests.post(REGISTER_URL, json={"email": email, "password": password}, timeout=15)
                if resp.status_code == 200:
                    st.success("Registered. Please log in.")
                else:
                    st.error(resp.text)
            except Exception as exc:
                st.error(f"Register failed: {exc}")
    else:
        exp = _jwt_expiry(st.session_state.auth_token)
        if exp:
            remaining = exp - int(time.time())
            mins = max(0, remaining // 60)
            st.caption(f"Token expires in ~{mins} min")
            if remaining < 300:
                last = st.session_state.get("last_refresh_attempt", 0)
                if time.time() - last > 60:
                    headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
                    refresh = requests.post(REFRESH_URL, headers=headers, timeout=10)
                    st.session_state["last_refresh_attempt"] = time.time()
                    if refresh.status_code == 200:
                        st.session_state.auth_token = refresh.json().get("access_token")
                        st.success("Token refreshed automatically")
        if st.button("Refresh Token"):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
                resp = requests.post(REFRESH_URL, headers=headers, timeout=15)
                if resp.status_code == 200:
                    st.session_state.auth_token = resp.json().get("access_token")
                    st.success("Token refreshed")
                else:
                    st.error(resp.text)
            except Exception as exc:
                st.error(f"Refresh failed: {exc}")
        if st.button("Logout"):
            st.session_state.auth_token = None
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())

# Session Browser
if st.session_state.auth_token:
    headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
    with st.sidebar:
        st.subheader("Sessions")
        if st.button("New Session"):
            try:
                resp = safe_request("POST", SESSIONS_URL, headers=headers, timeout=15)
                if resp.status_code == 200:
                    st.session_state.session_id = resp.json().get("session_id")
                    st.session_state.messages = []
                else:
                    st.error(resp.text)
            except Exception as exc:
                st.error(f"Session create failed: {exc}")
        try:
            resp = safe_request("GET", SESSIONS_URL, headers=headers, timeout=15)
            if resp.status_code == 200:
                sessions = resp.json().get("sessions", [])
                session_ids = [s["id"] for s in sessions]
                if session_ids:
                    selected = st.selectbox("Load Session", session_ids, index=0)
                    if st.button("Load"):
                        detail = safe_request(
                            "GET",
                            f"{SESSIONS_URL}/{selected}",
                            headers=headers,
                            timeout=15,
                        )
                        if detail.status_code == 200:
                            st.session_state.session_id = selected
                            data = detail.json()
                            st.session_state.messages = []
                            for ev in data.get("events", []):
                                content = ev.get("content")
                                if not content:
                                    continue
                                role = content.get("role")
                                parts = content.get("parts") or []
                                if not parts:
                                    continue
                                text = parts[0].get("text", "")
                                if role and text:
                                    st.session_state.messages.append({"role": role, "content": text})
                        else:
                            st.error(detail.text)
        except Exception:
            pass

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Handler
if prompt := st.chat_input("Ask about Google ADK..."):
    if not st.session_state.auth_token:
        st.error("Please log in first.")
        st.stop()
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Call Backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
                response = safe_request(
                    "POST",
                    BACKEND_URL,
                    json={"message": prompt, "session_id": st.session_state.session_id},
                    headers=headers,
                    timeout=60,
                )
                if response.status_code == 200:
                    data = response.json()
                    bot_text = data.get("response", "Error: No response text.")
                    st.markdown(bot_text)
                    st.session_state.messages.append({"role": "assistant", "content": bot_text})
                else:
                    err_msg = f"Error {response.status_code}: {response.text}"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
            except Exception as e:
                st.error(f"Connection Error: {e}")

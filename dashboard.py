import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Moonshot Live Tracker", layout="wide")
st.title("🚀 Moonshot Live Tracker")

# Funkcja pobierająca dane z bazy (odświeżana co 60 sekund)
@st.cache_data(ttl=60)
def load_data():
    try:
        conn = sqlite3.connect("moonshot_shadow.db")
        # Pobieramy tylko najważniejsze kolumny do podglądu
        query = """
            SELECT ticker, form, filing_date, moonshot_direction, moonshot_confidence, status, error 
            FROM moonshot_results 
            ORDER BY id DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return None

df = load_data()

if df is not None and not df.empty:
    col1, col2, col3 = st.columns(3)
    
    total_signals = len(df)
    executed_signals = len(df[df['status'] == 'ok'])
    errors = len(df[df['status'] == 'error'])
    
    col1.metric("Wszystkie Przeanalizowane Raporty", total_signals)
    col2.metric("Sygnały Zrealizowane (OK)", executed_signals)
    col3.metric("Błędy (API/Odrzucone)", errors)
    
    st.subheader("Ostatnie operacje w tle")
    # Formatowanie tabeli
    st.dataframe(
        df,
        column_config={
            "ticker": "Spółka",
            "form": "Dokument",
            "filing_date": "Data publikacji",
            "moonshot_direction": "Kierunek (LLM)",
            "moonshot_confidence": st.column_config.NumberColumn("Ufność (Confidence)", format="%.2f"),
            "status": "Status Egzekucji",
            "error": "Log Błędów"
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Oczekiwanie na dane. Baza moonshot_shadow.db jest pusta lub niedostępna.")

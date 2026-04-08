import streamlit as st
import os
import json
import pandas as pd
import altair as alt
from pathlib import Path
from juniorfetch.core.palace import MemoryPalace
from juniorfetch.core.crawler import JuniorFetchCrawler

st.set_page_config(page_title="JuniorFetch | Sovereign Node", layout="wide")
st.title("📂 JuniorFetch: Sovereign TDA File Command")

palace = MemoryPalace()
crawler = JuniorFetchCrawler()

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Search & Edit", 
    "🗂️ Registry Snapshot", 
    "🧬 FSD Heart (Telemetry)", 
    "⚙️ Disk Indexer"
])

# TAB 1: Local Search & Live Editor
with tab1:
    st.subheader("Semantic Bit Drift Search")
    query = st.text_input("Query your local mesh (e.g., 'trading strategy', 'deployment config'):")
    
    if st.button("Execute Vector Search") and query:
        results = palace.semantic_search(query, wing="files")
        st.write(f"**Found {len(results)} coherent file states.**")
        
        for idx, r in enumerate(results[:15]):
            path_str = r['metadata'].get('path', 'Unknown Path')
            q_mark = r.get('q_mark', 0.0)
            
            with st.expander(f"📄 {path_str} | Q-Mark: {q_mark}"):
                file_path = Path(path_str)
                
                # Check if file still exists on actual disk
                if file_path.exists():
                    current_text = file_path.read_text(errors="ignore")
                    
                    # Live Editor
                    edited_text = st.text_area(
                        "Live File Editor (Saves to Disk & Mesh)", 
                        current_text, 
                        height=250, 
                        key=f"edit_{idx}"
                    )
                    
                    if st.button("Save Edit & Re-Etch", key=f"save_{idx}"):
                        try:
                            # 1. Save to physical disk
                            file_path.write_text(edited_text, encoding="utf-8")
                            
                            # 2. Re-etch into TDA memory palace
                            hall_name = r['metadata'].get('hall', 'root')
                            palace.store(
                                wing="files",
                                hall=hall_name,
                                room=file_path.name,
                                content=edited_text,
                                metadata=r['metadata']
                            )
                            st.success("✅ File updated on disk and re-synchronized with TDA Mesh.")
                        except Exception as e:
                            st.error(f"Failed to write: {e}")
                else:
                    st.warning("⚠️ File no longer exists on physical disk. Showing last cached mesh state.")
                    st.code(r['content'][:2000])

# TAB 2: Registry Snapshot (Directory Browser)
with tab2:
    st.subheader("Topological Registry Browser")
    st.info("Browse the exact directories mapped by the Omni Math kernel.")
    
    wing_path = palace.root / "files"
    if wing_path.exists():
        halls = sorted([d.name for d in wing_path.iterdir() if d.is_dir()])
        selected_hall = st.selectbox("Select Indexed Directory Segment (Hall)", ["-- Select --"] + halls)
        
        if selected_hall != "-- Select --":
            hall_path = wing_path / selected_hall
            rooms = sorted([d.name for d in hall_path.iterdir() if d.is_dir()])
            
            st.write(f"**Tracked Files in Segment:** {len(rooms)}")
            for room in rooms[:50]:  # Limit display for performance
                drawer = hall_path / room / "drawers.jsonl"
                if drawer.exists():
                    st.markdown(f"- 📝 `{room}`")
    else:
        st.warning("No files indexed yet. Run the crawler.")

# TAB 3: FSD Heart (TDA Quant Projections)
with tab3:
    st.subheader("🧬 FSD Heart: Manifold Topology Spread")
    
    @st.cache_data(ttl=60)
    def fetch_mesh_telemetry():
        wing_path = palace.root / "files"
        data = []
        if wing_path.exists():
            for drawer_file in wing_path.rglob("drawers.jsonl"):
                try:
                    with open(drawer_file, "r") as f:
                        for line in f:
                            obj = json.loads(line)
                            data.append({
                                "Extension": obj["metadata"].get("extension", "unknown"),
                                "Q_Mark": obj.get("q_mark", 0.0),
                                "Size_KB": obj["metadata"].get("size_bytes", 0) / 1024
                            })
                except: pass
        return pd.DataFrame(data)

    if st.button("Scan Mesh Telemetry"):
        df = fetch_mesh_telemetry()
        
        if not df.empty:
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Meshed Tensors", f"{len(df):,}")
            m2.metric("Mean Q-Mark Intensity", f"{df['Q_Mark'].mean():.3f}")
            m3.metric("Total Indexed Size", f"{df['Size_KB'].sum() / 1024:.2f} MB")
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("**File Type Distribution**")
                ext_counts = df['Extension'].value_counts().reset_index()
                ext_counts.columns = ['Extension', 'Count']
                chart = alt.Chart(ext_counts).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="Count", type="quantitative"),
                    color=alt.Color(field="Extension", type="nominal"),
                    tooltip=['Extension', 'Count']
                )
                st.altair_chart(chart, use_container_width=True)
                
            with c2:
                st.markdown("**Q-Mark Quantum Signal Density**")
                hist = alt.Chart(df).mark_bar().encode(
                    alt.X("Q_Mark:Q", bin=alt.Bin(maxbins=30), title="Signal Intensity (Q-Mark)"),
                    alt.Y('count()', title="Node Count"),
                    tooltip=['count()']
                ).interactive()
                st.altair_chart(hist, use_container_width=True)
        else:
            st.info("Mesh is empty. Please index files to generate telemetry.")

# TAB 4: Disk Indexer
with tab4:
    st.subheader("Directory Crawler")
    target_dir = st.text_input("Target Directory to Index", "~/Documents")
    max_f = st.number_input("Max Files to Target", 100, 500000, 10000)
    
    if st.button("Run Indexer"):
        with st.spinner(f"Crawling {target_dir}..."):
            crawler.index(target_dir, max_files=int(max_f))
            st.success("Indexing complete. Telemetry available in FSD Heart.")
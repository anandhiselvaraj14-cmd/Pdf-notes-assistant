import streamlit as st
import pymupdf

st.set_page_config(page_title="PDF Notes Assistant", page_icon="📚")
st.title("📚 PDF Notes Assistant")
st.write("Upload text-based PDF notes. Create a simple summary, key points, or revision questions.")

pdf = st.file_uploader("Choose a PDF from your phone", type=["pdf"])
if pdf:
    try:
        doc = pymupdf.open(stream=pdf.getvalue(), filetype="pdf")
        text = "\n".join(page.get_text() for page in doc).strip()
        st.caption(f"Pages: {len(doc)}")
        if not text:
            st.warning("Text extract aagala. Idhu scanned/image PDF-a irukkalaam; indha starter version OCR support pannaadhu.")
        else:
            mode = st.selectbox("Enna create pannanum?", ["Summary", "Key points", "Quiz questions"])
            if st.button("Create"):
                lines = [s.strip() for s in text.splitlines() if s.strip()]
                if mode == "Summary":
                    st.subheader("Simple preview summary")
                    st.write("\n\n".join(lines[:8]))
                elif mode == "Key points":
                    st.subheader("Key points")
                    for line in [x for x in lines if len(x)>25][:10]: st.write("• " + line[:300])
                else:
                    st.subheader("Revision prompts")
                    for i,line in enumerate([x for x in lines if len(x)>25][:5],1): st.write(f"{i}. Explain: {line[:250]}")
            with st.expander("Extracted text preview"):
                st.text(text[:8000])
            st.info("Prototype note: This uses simple text extraction, not an AI model. Please verify study notes against the original PDF.")
    except Exception as e:
        st.error(f"PDF read panna mudiyala: {e}")

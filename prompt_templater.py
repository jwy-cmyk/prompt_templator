import streamlit as st
import textwrap
import html

# ===== 개발자 설정 영역 =====
TOOL_OPTIONS = [
    "목록형 TO 서술형 재작성",
    "질의 재구성",
]

PROMPT_TOOL_URL = "https://your-prompt-runner.example.com"  # 결과 확인용 링크
APP_TITLE = "프롬프트 템플레이터"
# ==========================


def main():
    st.set_page_config(page_title=APP_TITLE, layout="centered")
    st.title(APP_TITLE)

    st.markdown("프롬프트를 미리 템플릿 형태로 만들어 복사해서 사용할 수 있는 도구입니다.")

    # ---- 입력 영역 ----
    st.subheader("1. 입력값")

    selected_llm = st.selectbox("요청 LLM", TOOL_OPTIONS, index=0)

    user_query = st.text_area(
        "질의",
        height=120,
        placeholder="수정할 턴의 질의를 입력하세요.",
    )

    model_answer = st.text_area(
        "모델 답변",
        height=160,
        placeholder="수정할 턴의 모델 답변을 입력하세요.",
    )

    st.markdown("---")

    # ---- 프롬프트 생성 ----
    st.subheader("2. 생성된 프롬프트")

    if not user_query and not model_answer:
        st.info("질의와 모델 답변을 입력하면 프롬프트가 생성됩니다.")
        return

    # 템플릿은 상황에 맞게 수정해서 사용하면 됩니다.
    combined_prompt = textwrap.dedent(f"""
    [요청 TOOL]
    {selected_llm}

    [질의]
    {user_query.strip()}

    [모델 답변]
    {model_answer.strip()}

    위 내용을 하나의 프롬프트로 사용하세요.
    {PROMPT_TOOL_URL}에서 프롬프트를 입력하여 결과를 확인하세요.
    """).strip()

    # 프롬프트 표시
    st.text_area(
        "최종 프롬프트",
        value=combined_prompt,
        height=260,
    )

    # ---- 복사 버튼 + 알림 (JS 이용) ----
    st.markdown("#### 3. 복사")

    # JS에 넣기 위해 최소한의 escape
    safe_text = (
        combined_prompt
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("</script>", "<\\/script>")
    )
    safe_text = html.escape(safe_text)  # html 이스케이프

    from streamlit import components
    components.v1.html(
        f"""
        <div>
          <button 
            onclick="(function() {{
                const text = `{safe_text}`;
                navigator.clipboard.writeText(text).then(function() {{
                    alert('복사되었습니다.');
                }}, function(err) {{
                    alert('복사에 실패했습니다. 브라우저에서 직접 Ctrl+C / Cmd+C를 이용해 복사해 주세요.');
                }});
            }})()"
            style="
                padding: 8px 16px;
                border-radius: 4px;
                border: 1px solid #ccc;
                cursor: pointer;
                font-size: 14px;
            "
          >
            프롬프트 복사하기
          </button>
        </div>
        """,
        height=60,
    )

    st.caption(f"또는 위 텍스트를 드래그 후 복사한 뒤, **{PROMPT_TOOL_URL}** 에서 프롬프트를 입력하여 결과를 확인하세요.")


if __name__ == "__main__":
    main()

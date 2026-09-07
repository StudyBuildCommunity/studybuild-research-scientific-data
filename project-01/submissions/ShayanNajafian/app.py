"""Student-facing Streamlit prototype for contextual stress-risk estimation."""

from pathlib import Path

import streamlit as st

from src.prediction import load_model_bundle, predict_stress


ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "stress_risk_pipeline.joblib"
METADATA_PATH = ROOT / "models" / "stress_risk_model_metadata.json"

QUESTION_GROUPS = {
    "Academic context": [
        {
            "feature": "study_load",
            "label": "How heavy does your current study load feel?",
            "low": "lowest recorded load",
            "high": "heaviest recorded load",
        },
        {
            "feature": "teacher_student_relationship",
            "label": "How strong is your relationship with your teachers?",
            "low": "weakest recorded relationship",
            "high": "strongest recorded relationship",
        },
        {
            "feature": "extracurricular_activities",
            "label": "How frequently do you participate in extracurricular activities?",
            "low": "least frequent participation",
            "high": "most frequent participation",
        },
    ],
    "Social context": [
        {
            "feature": "bullying",
            "label": "How severe is the bullying you currently experience?",
            "low": "lowest recorded severity",
            "high": "highest recorded severity",
        },
        {
            "feature": "social_support",
            "label": "How strong is your current social support?",
            "low": "lowest recorded support",
            "high": "strongest recorded support",
        },
        {
            "feature": "peer_pressure",
            "label": "How intense is the peer pressure you experience?",
            "low": "lowest recorded pressure",
            "high": "most intense recorded pressure",
        },
    ],
    "Environmental context": [
        {
            "feature": "noise_level",
            "label": "How noisy is your usual environment?",
            "low": "quietest recorded environment",
            "high": "loudest recorded environment",
        },
        {
            "feature": "living_conditions",
            "label": "How would you rate your living conditions?",
            "low": "poorest recorded conditions",
            "high": "best recorded conditions",
        },
        {
            "feature": "safety",
            "label": "How safe do you feel in your usual environment?",
            "low": "lowest recorded safety",
            "high": "highest recorded safety",
        },
        {
            "feature": "basic_needs",
            "label": "How well are your basic needs currently being met?",
            "low": "lowest recorded satisfaction",
            "high": "highest recorded satisfaction",
        },
    ],
}

RESULT_COPY = {
    "Low": {
        "heading": "Lower stress-risk pattern",
        "message": (
            "Your answers resemble students labeled Low stress in this dataset. "
            "This does not rule out stress or replace your own judgment."
        ),
        "kind": "success",
    },
    "Medium": {
        "heading": "Moderate stress-risk pattern",
        "message": (
            "Your answers resemble students labeled Medium stress in this dataset. "
            "Early support or a conversation with someone you trust may help prevent escalation."
        ),
        "kind": "warning",
    },
    "High": {
        "heading": "Elevated stress-risk pattern",
        "message": (
            "Your answers resemble students labeled High stress in this dataset. "
            "Consider seeking timely support from someone you trust or an appropriate student service."
        ),
        "kind": "error",
    },
}


st.set_page_config(
    page_title="Student Stress Context Check",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1080px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }
        .hero {
            padding: 1.6rem 1.7rem;
            border: 1px solid rgba(63, 102, 88, 0.18);
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(224, 242, 235, 0.92), rgba(245, 249, 247, 0.96));
            margin-bottom: 1.35rem;
        }
        .hero h1 {
            color: #173f35;
            font-size: clamp(2rem, 5vw, 3.1rem);
            letter-spacing: -0.035em;
            margin: 0 0 0.35rem 0;
        }
        .hero p {
            color: #3d5e55;
            font-size: 1.08rem;
            margin: 0;
            max-width: 760px;
        }
        .scale-note {
            color: #63766f;
            font-size: 0.84rem;
            margin-top: -0.55rem;
            margin-bottom: 1rem;
        }
        .result-card {
            border: 1px solid rgba(23, 63, 53, 0.16);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            background: rgba(248, 251, 250, 0.95);
        }
        .result-eyebrow {
            color: #63766f;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .result-title {
            color: #173f35;
            font-size: 1.65rem;
            font-weight: 750;
            margin-top: 0.2rem;
        }
        div[data-testid="stForm"] {
            border: 1px solid rgba(23, 63, 53, 0.14);
            border-radius: 16px;
            padding: 1.25rem 1.35rem 1.45rem;
            background: rgba(255, 255, 255, 0.82);
        }
        div[data-testid="stSidebar"] {
            background: #f5f8f7;
        }
        .footer-note {
            color: #6b7f78;
            font-size: 0.82rem;
            text-align: center;
            margin-top: 2.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def load_assets():
    return load_model_bundle(MODEL_PATH, METADATA_PATH)


try:
    model, metadata = load_assets()
except (FileNotFoundError, ValueError, OSError) as error:
    st.error(f"The application model could not be loaded: {error}")
    st.stop()


def render_question(question: dict[str, str]) -> int:
    feature = question["feature"]
    allowed_values = metadata["input_schema"][feature]["allowed_values"]
    selected_value = st.select_slider(
        question["label"],
        options=allowed_values,
        value=allowed_values[len(allowed_values) // 2],
        key=f"input_{feature}",
        help=(
            "Choose the closest code. Intermediate numbers are ordinal dataset "
            "values rather than clinically validated cutoffs."
        ),
    )
    st.markdown(
        f'<div class="scale-note">{allowed_values[0]} = {question["low"]} · '
        f'{allowed_values[-1]} = {question["high"]}</div>',
        unsafe_allow_html=True,
    )
    return int(selected_value)


st.markdown(
    """
    <section class="hero">
        <h1>Student Stress Context Check</h1>
        <p>
            Explore how your academic, social, and environmental circumstances
            compare with patterns in a student-stress dataset.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.info(
    "This portfolio prototype estimates a dataset pattern—not a diagnosis. "
    "It should never be used for automatic academic, disciplinary, or clinical decisions."
)

with st.sidebar:
    st.header("About this check")
    st.markdown(
        "- Uses **10 contextual inputs**\n"
        "- Does **not** request mental-health history\n"
        "- Does **not intentionally store** your answers\n"
        "- Uses a weighted logistic-regression pipeline"
    )
    st.divider()
    st.caption(
        "Model evaluation: 85.1% High-stress recall and 93.8% Elevated-stress "
        "recall on the frozen 220-student test set. Real-world reliability is unverified."
    )

with st.expander("How should I use the numeric scales?"):
    st.markdown(
        "The sliders follow the direction and ranges documented for this dataset. "
        "Exact verbal meanings for every intermediate code were not provided, so "
        "choose the number that best represents your position between the endpoints. "
        "[Read the published variable descriptions](https://www.frontiersin.org/"
        "journals/psychology/articles/10.3389/fpsyg.2025.1684529/full)."
    )

with st.form("stress_context_form", clear_on_submit=False):
    answers: dict[str, int] = {}
    for group_name, questions in QUESTION_GROUPS.items():
        st.subheader(group_name)
        columns = st.columns(2)
        for index, question in enumerate(questions):
            with columns[index % 2]:
                answers[question["feature"]] = render_question(question)

    submitted = st.form_submit_button(
        "Estimate my stress-risk pattern",
        type="primary",
        use_container_width=True,
    )

if submitted:
    try:
        result = predict_stress(answers, model, metadata)
    except ValueError as error:
        st.error(f"Please review your answers: {error}")
    else:
        result_copy = RESULT_COPY[result["predicted_label"]]
        st.divider()
        st.markdown(
            '<div class="result-card">'
            '<div class="result-eyebrow">Estimated dataset category</div>'
            f'<div class="result-title">{result_copy["heading"]}</div>'
            "</div>",
            unsafe_allow_html=True,
        )
        getattr(st, result_copy["kind"])(result_copy["message"])

        st.subheader("Model probability distribution")
        for label in ("Low", "Medium", "High"):
            probability = result["probabilities"][label]
            st.markdown(f"**{label}** — {probability:.1%}")
            st.progress(float(probability))

        st.caption(
            "These percentages are model probabilities within this dataset. "
            "They are not clinical probabilities and may not transfer to other student populations."
        )

        st.subheader("A supportive next step")
        if result["predicted_label"] == "Low":
            st.write(
                "Continue noticing changes in your workload, support, safety, and living "
                "conditions. Seek support whenever you feel you need it, regardless of this result."
            )
        else:
            st.write(
                "Consider checking in with someone you trust, a student-support service, "
                "or a qualified professional. Asking early can help prevent stress from becoming harder to manage."
            )

        st.warning(
            "If you may be in immediate danger or might harm yourself, contact local "
            "emergency services or an appropriate crisis service now."
        )

st.markdown(
    '<div class="footer-note">Educational portfolio prototype · Responses are processed for the current result only</div>',
    unsafe_allow_html=True,
)

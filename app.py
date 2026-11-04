```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}
[data-testid="stMetric"] {
    background: #f4f7fb;
    padding: 16px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏥 Hospital Management System")
st.caption("Manage patients, doctors, appointments, treatments and billing.")

# Generate Demo Dataset

@st.cache_data
def load_demo():

    rng = np.random.default_rng(42)

    n = 500

    departments = [
        "Cardiology",
        "Neurology",
        "Orthopedics",
        "Pediatrics",
        "General Medicine"
    ]

    patient = pd.DataFrame({
        "PatientID": [f"P{i:04d}" for i in range(1, n+1)],
        "PatientName": [f"Patient {i}" for i in range(1, n+1)],
        "Age": rng.integers(1, 90, n),
        "Gender": rng.choice(["Male", "Female", "Other"], n),
        "Department": rng.choice(departments, n),
        "Doctor": rng.choice(
            ["Dr. Ravi", "Dr. Priya", "Dr. Kumar", "Dr. Sneha"],
            n
        ),
        "AppointmentDate": pd.date_range(
            "2026-01-01", periods=n, freq="D"
        ),
        "AppointmentStatus": rng.choice(
            ["Completed", "Pending", "Cancelled"],
            n,
            p=[0.65, 0.25, 0.10]
        ),
        "Treatment": rng.choice(
            ["General Checkup", "Surgery", "Consultation",
             "Medication", "Therapy"],
            n
        ),
        "MedicineCost": np.round(rng.uniform(100, 3000, n), 2),
        "TreatmentCost": np.round(rng.uniform(500, 10000, n), 2),
        "BillAmount": np.round(rng.uniform(1000, 20000, n), 2)
    })

    return patient


# Sidebar

with st.sidebar:

    st.header("Data Source")

    upload = st.file_uploader(
        "Upload Hospital CSV",
        type=["csv"]
    )

    st.info(
        "The application uses synthetic demo records "
        "when no CSV file is uploaded."
    )

    st.header("Filters")


# Load Dataset

if upload is not None:

    try:
        raw = pd.read_csv(upload)
        source_label = f"Uploaded file: {upload.name}"

    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        st.stop()

else:

    raw = load_demo()
    source_label = "Synthetic Demonstration Dataset"


st.caption(source_label)

df = raw.copy()


# Sidebar Filters

with st.sidebar:

    if "Department" in df.columns:

        opts = sorted(
            df["Department"].dropna().astype(str).unique()
        )

        selected = st.multiselect(
            "Department",
            opts,
            default=opts
        )

        df = df[
            df["Department"].astype(str).isin(selected)
        ]

    if "Gender" in df.columns:

        opts = sorted(
            df["Gender"].dropna().astype(str).unique()
        )

        selected = st.multiselect(
            "Gender",
            opts,
            default=opts
        )

        df = df[
            df["Gender"].astype(str).isin(selected)
        ]

    if "Age" in df.columns and pd.api.types.is_numeric_dtype(df["Age"]) and not df["Age"].dropna().empty:

        lo = int(df["Age"].min())
        hi = int(df["Age"].max())

        age_range = st.slider(
            "Patient Age",
            lo,
            hi,
            (lo, hi)
        )

        df = df[
            df["Age"].between(*age_range)
        ]


# Dashboard Tabs

tabs = st.tabs([
    "Overview",
    "Patient Data",
    "Data Quality",
    "Visualizations",
    "About"
])


# TAB 1: OVERVIEW

with tabs[0]:

    st.subheader("Hospital Overview")

    a, b, c, d = st.columns(4)

    a.metric(
        "Total Patients",
        f"{len(df):,}"
    )

    b.metric(
        "Departments",
        f"{df['Department'].nunique()}"
        if "Department" in df.columns else "N/A"
    )

    if "BillAmount" in df.columns:
        c.metric(
            "Total Revenue",
            f"₹{df['BillAmount'].sum():,.2f}"
        )
    else:
        c.metric("Total Revenue", "N/A")

    if "AppointmentStatus" in df.columns:
        d.metric(
            "Appointments",
            f"{len(df):,}"
        )
    else:
        d.metric("Appointments", "N/A")


    left, right = st.columns(2)

    if "Department" in df.columns:

        counts = (
            df["Department"]
            .fillna("Missing")
            .value_counts()
            .rename_axis("Department")
            .reset_index(name="Patients")
        )

        left.plotly_chart(
            px.bar(
                counts,
                x="Department",
                y="Patients",
                title="Patients by Department"
            ),
            use_container_width=True
        )

    if "Gender" in df.columns:

        counts = (
            df["Gender"]
            .fillna("Missing")
            .value_counts()
            .rename_axis("Gender")
            .reset_index(name="Patients")
        )

        right.plotly_chart(
            px.pie(
                counts,
                names="Gender",
                values="Patients",
                title="Gender Distribution"
            ),
            use_container_width=True
        )


    st.markdown("#### Patient Statistics")

    st.dataframe(
        df.describe(include="all").transpose(),
        use_container_width=True
    )


# TAB 2: PATIENT DATA

with tabs[1]:

    st.subheader("Patient Records")

    st.write(
        f"Showing **{len(df):,}** patient records."
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=440
    )

    csv_bytes = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Patient Data",
        csv_bytes,
        "hospital_patient_data.csv",
        "text/csv"
    )

    search = st.text_input(
        "Search Patient",
        placeholder="Enter Patient ID, name or department"
    )

    if search:

        mask = df.astype(str).apply(
            lambda col: col.str.contains(
                search,
                case=False,
                na=False
            )
        ).any(axis=1)

        st.dataframe(
            df[mask],
            use_container_width=True
        )


# TAB 3: DATA QUALITY

with tabs[2]:

    st.subheader("Data Quality and Cleaning")

    q1, q2, q3 = st.columns(3)

    q1.metric(
        "Total Rows",
        f"{len(raw):,}"
    )

    q2.metric(
        "Duplicate Rows",
        f"{int(raw.duplicated().sum()):,}"
    )

    q3.metric(
        "Missing Cells",
        f"{int(raw.isna().sum().sum()):,}"
    )


    quality = pd.DataFrame({

        "Column": raw.columns,

        "Data Type": [
            str(t) for t in raw.dtypes
        ],

        "Missing Values": raw.isna().sum().values,

        "Missing (%)": (
            raw.isna().mean().values * 100
        ).round(2),

        "Unique Values": raw.nunique(
            dropna=True
        ).values

    })

    st.dataframe(
        quality,
        use_container_width=True
    )


    st.markdown("#### Create Cleaned Dataset")

    fill_missing = st.checkbox(
        "Fill missing numeric values with median"
    )

    remove_duplicates = st.checkbox(
        "Remove duplicate rows",
        value=True
    )

    cleaned = raw.copy()

    if remove_duplicates:

        cleaned = cleaned.drop_duplicates()

    if fill_missing:

        for col in cleaned.select_dtypes(
            include="number"
        ).columns:

            if cleaned[col].isna().any():

                cleaned[col] = cleaned[col].fillna(
                    cleaned[col].median()
                )


    st.success(
        f"Cleaned Dataset: {len(cleaned):,} rows "
        f"and {cleaned.isna().sum().sum():,} missing cells remain."
    )

    st.download_button(
        "Download Cleaned Dataset",
        cleaned.to_csv(index=False).encode("utf-8"),
        "cleaned_hospital_data.csv",
        "text/csv"
    )


# TAB 4: VISUALIZATIONS

with tabs[3]:

    st.subheader("Hospital Data Visualizations")

    numeric_cols = list(
        df.select_dtypes(include="number").columns
    )

    categorical_cols = list(
        df.select_dtypes(exclude="number").columns
    )


    if numeric_cols:

        xcol = st.selectbox(
            "Select Numeric Variable",
            numeric_cols
        )

        st.plotly_chart(
            px.histogram(
                df,
                x=xcol,
                title=f"Distribution of {xcol}",
                marginal="box"
            ),
            use_container_width=True
        )


    if len(numeric_cols) >= 2:

        x, y = st.columns(2)

        xcol = x.selectbox(
            "X-axis",
            numeric_cols,
            index=0
        )

        ycol = y.selectbox(
            "Y-axis",
            numeric_cols,
            index=1
        )

        st.plotly_chart(
            px.scatter(
                df,
                x=xcol,
                y=ycol,
                title=f"{ycol} vs {xcol}"
            ),
            use_container_width=True
        )


    if categorical_cols:

        cat = st.selectbox(
            "Select Category",
            categorical_cols
        )

        counts = (
            df[cat]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .rename_axis(cat)
            .reset_index(name="Count")
        )

        st.plotly_chart(
            px.bar(
                counts,
                x=cat,
                y="Count",
                title=f"Records by {cat}"
            ),
            use_container_width=True
        )


    if len(numeric_cols) >= 2:

        st.markdown("#### Correlation Matrix")

        st.plotly_chart(
            px.imshow(
                df[numeric_cols].corr(
                    numeric_only=True
                ),
                text_auto=".2f",
                aspect="auto",
                title="Numeric Correlation Matrix"
            ),
            use_container_width=True
        )


# TAB 5: ABOUT

with tabs[4]:

    st.subheader("About Hospital Management System")

    st.write("""
    This project is a Hospital Management System
    developed using Python and Streamlit.

    It helps analyze hospital information,
    patient records, appointments, departments,
    treatments and billing information.
    """)

    st.markdown("#### Technologies Used")

    st.write("""
    - Python
    - Pandas
    - NumPy
    - Streamlit
    - Plotly
    """)

    st.markdown("#### Main Features")

    st.write("""
    1. Patient Data Management
    2. Department-wise Patient Analysis
    3. Appointment Analysis
    4. Treatment and Billing Analysis
    5. Data Cleaning
    6. Interactive Visualizations
    7. CSV File Upload and Download
    """)

    st.warning(
        "This application uses synthetic demonstration "
        "data. It is an analytics dashboard, not a complete "
        "clinical or hospital record-management system. "
        "Do not upload real patient information unless "
        "the environment is authorized and approved."
    )
```

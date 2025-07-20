import pandas as pd
from sqlalchemy import MetaData, Table, Column, Integer, Float, String, DateTime
import io
import streamlit as st

def render():
    st.header("📥 데이터 업로드 및 스키마 자동생성")
    st.write("여기에 파일 업로드 및 스키마 추출 UI가 들어갑니다.")

def pandas_dtype_to_sqla(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return Integer
    elif pd.api.types.is_float_dtype(dtype):
        return Float
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return DateTime
    else:
        return String(255)

def infer_schema_from_file(file) -> pd.DataFrame:
    # 파일 확장자별 판별
    filename = file.filename
    if filename.endswith('.csv'):
        df = pd.read_csv(file.file)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(file.file)
    elif filename.endswith('.json'):
        df = pd.read_json(file.file)
    else:
        raise ValueError("지원하지 않는 파일 형식입니다.")
    # 컬럼, 타입 추출 (for UI 미리보기)
    schema = [{"col": col, "dtype": str(df[col].dtype)} for col in df.columns]
    return schema, df

def auto_create_schema_from_df(df, table_name, engine):
    metadata = MetaData()
    columns = [
        Column(col, pandas_dtype_to_sqla(df[col].dtype))
        for col in df.columns
    ]
    table = Table(table_name, metadata, *columns)
    metadata.create_all(engine)
    # 데이터 저장도 원하면...
    df.to_sql(table_name, engine, if_exists='append', index=False)
    return f"테이블 '{table_name}' 생성 및 데이터 저장 완료"

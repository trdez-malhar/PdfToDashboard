import time
import pandas as pd
def restructure_data(table_data : list):
    """para list of tables"""
    result = {"table_layout" : [], "table_grid_layout" : []}
    for table in table_data:
        table_num = int(table["self_ref"][-1:])
        page_num = table["prov"][0]["page_no"]

        # Create a new instance for each table layout
        table_layout_data = {
            "table_no": table_num,
            "page_no": page_num,
            "table_bbox_l": table["prov"][0]["bbox"].get("l", None),
            "table_bbox_t": table["prov"][0]["bbox"].get("t", None),
            "table_bbox_r": table["prov"][0]["bbox"].get("r", None),
            "table_bbox_b": table["prov"][0]["bbox"].get("b", None),
            "table_coord_origin": table["prov"][0]["bbox"].get("coord_origin", None),
            "num_rows": table["data"]["num_rows"],
            "num_cols": table["data"]["num_cols"],
        }

        result["table_layout"].append(table_layout_data)

        # Process grid data
        grid_data = [cell for row in table["data"]["grid"] for cell in row]
        for cell_data in grid_data:
            # Create a new instance for each cell
            table_griddata_layout = {
                "table_no": table_num,
                "page_no": page_num,
                "l": cell_data.get("bbox", {}).get("l", None),
                "t": cell_data.get("bbox", {}).get("t", None),
                "r": cell_data.get("bbox", {}).get("r", None),
                "b": cell_data.get("bbox", {}).get("b", None),
                "coord_origin": cell_data.get("bbox", {}).get("coord_origin", None),
                "row_span": cell_data.get("row_span", None),
                "col_span": cell_data.get("col_span", None),
                "start_row_offset_idx": cell_data.get("start_row_offset_idx", None),
                "end_row_offset_idx": cell_data.get("end_row_offset_idx", None),
                "start_col_offset_idx": cell_data.get("start_col_offset_idx", None),
                "end_col_offset_idx": cell_data.get("end_col_offset_idx", None),
                "text": cell_data.get("text", None),
                "column_header": cell_data.get("column_header", None),
                "row_header": cell_data.get("row_header", None),
                "row_section": cell_data.get("row_section", None),
            }
            result["table_grid_layout"].append(table_griddata_layout)

    return result


def transform(result_data):
    table_level_df = pd.DataFrame(result_data["table_layout"])
    save(table_level_df, "table_level")
    transform_data_df = clean_up(result_data)
    #table name mapping
    # Predefined table mapping for known table_no values (0-4)
    transform_data_df = table_name_mapping(transform_data_df)
    save(transform_data_df, "cell_level")
    # Aggregate table features
    table_df = aggregate_table_cell_data(transform_data_df)
    # Flatten MultiIndex column names
    table_df = flatten_multiindex(table_df)
    # Merge with table-level data
    merged_df = table_level_df.merge(table_df, on=['page_no', 'table_no'], how='left')
    return merged_df

def save(df, type):
    timestamp = time.time_ns()
    df.to_csv(f"{OUTPUT_CLEAN_FOLDER}{timestamp}_{type}.csv", index=False)

def flatten_multiindex(table_df):
    table_df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in table_df.columns]
    table_df.rename(columns={"table_no_" : "table_no", "page_no_":"page_no", "table_name_" : "table_name"}, inplace=True)
    return table_df

def aggregate_table_cell_data(transform_data_df):
    table_df = transform_data_df.groupby(['page_no', 'table_no', 'table_name']).agg({
        'row_span': ['mean', 'max', 'min'],   
        'col_span': ['mean', 'max', 'min'],   
        'start_row_offset_idx': ['mean', 'max', 'min'],
        'end_row_offset_idx': ['mean', 'max', 'min'],
        'start_col_offset_idx': ['mean', 'max', 'min'],
        'end_col_offset_idx': ['mean', 'max', 'min'],
        'l': ['mean', 'max', 'min'],
        't': ['mean', 'max', 'min'],
        'r': ['mean', 'max', 'min'],
        'b': ['mean', 'max', 'min'],
        'column_header': ['sum', 'mean'],  # Total and percentage of column headers
        'row_header': ['sum', 'mean'],  # Total and percentage of row headers
    }).reset_index()
    
    return table_df

def table_name_mapping(transform_data_df):
    table_mapping = {
        0: "user_investment_summary",
        1: "accounts_detail",
        2: "portfolio_summary",
        3: "asset_allocation",
    }
    
    transform_data_df["table_name"] = transform_data_df["table_no"].map(table_mapping)
    cdsl_table_num = transform_data_df[transform_data_df["text"] == "ISINISIN"]["table_no"]
    transform_data_df.loc[transform_data_df["table_no"].isin(cdsl_table_num), "table_name"] = "cdsl_holdings"
    mf_table_num = transform_data_df[transform_data_df["text"] == "SchemeName"]["table_no"]
    transform_data_df.loc[transform_data_df["table_no"].isin(mf_table_num), "table_name"] = "mf_holdings"
    transform_data_df["table_name"] = transform_data_df["table_name"].fillna("unknown_table")
    return transform_data_df

def clean_up(result_data):
    transform_data_df = pd.DataFrame(result_data["table_grid_layout"])
    transform_data_df.loc[transform_data_df["column_header"], "text"] = (
        transform_data_df.loc[transform_data_df["column_header"], "text"]
        .astype(str)  # Convert to string to avoid None/NaN issues
        .str.replace(r"[^a-zA-Z]", "", regex=True)  # Remove non-English characters
    )

    boolean_columns = ["column_header", "row_header", "row_section"]
    transform_data_df[boolean_columns] = transform_data_df[boolean_columns].astype(int)
    return transform_data_df
import streamlit as st

# Section widths for 23-inch doors
section_data_23 = {
    "2 DR FULL FRAME": 48.625,
    "3 DR FULL FRAME": 72.25,
    "4 DR FULL FRAME": 95.6875,
    "2 DR LEFT": 48.25,
    "3 DR LEFT": 71.875,
    "4 DR LEFT": 95.3125,
    "2 DR CNTR": 47.875,
    "3 DR CNTR": 71.875,
    "4 DR CNTR": 95.3125,
    "2 DR RIGHT": 48.25,
    "3 DR RIGHT": 71.875,
    "4 DR RIGHT": 95.3125,
}

# Section widths for 30-inch doors
section_data_30 = {
    "2 DR FULL FRAME": 61.5,
    "3 DR FULL FRAME": 91.5625,
    "4 DR FULL FRAME": 121.4375,
    "2 DR LEFT": 61.125,
    "3 DR LEFT": 91.1875,
    "4 DR LEFT": 121.0625,
    "2 DR CNTR": 60.75,
    "3 DR CNTR": 91.1875,
    "4 DR CNTR": 121.0625,
    "2 DR RIGHT": 61.125,
    "3 DR RIGHT": 91.1875,
    "4 DR RIGHT": 121.0625,
}

def determine_sections_from_doors(door_count, section_data):
    if door_count == 2:
        return ["2 DR FULL FRAME"], section_data["2 DR FULL FRAME"]
    elif door_count == 3:
        return ["3 DR FULL FRAME"], section_data["3 DR FULL FRAME"]
    elif door_count == 4:
        return ["4 DR FULL FRAME"], section_data["4 DR FULL FRAME"]

    remaining = door_count
    if remaining % 2 == 1:
        right = 3
        left = remaining - right
    else:
        left = right = remaining // 2
        if remaining == 6:
            left = right = 3

    center = 0
    if left > 4:
        center += left - 4
        left = 4
    if right > 4:
        center += right - 4
        right = 4

    sections = [f"{left} DR LEFT"]
    while center > 0:
        if center >= 4:
            sections.append("4 DR CNTR")
            center -= 4
        elif center >= 3:
            sections.append("3 DR CNTR")
            center -= 3
        elif center >= 2:
            sections.append("2 DR CNTR")
            center -= 2
    sections.append(f"{right} DR RIGHT")
    total_width = sum(section_data.get(s, 0) for s in sections)
    return sections, round(total_width, 3)

# Web interface
st.title("Edge Door Lineup Configurator")

input_type = st.radio("Select Input Type", ["Target Net Opening", "Number of Doors"])

if input_type == "Target Net Opening":
    target_width = st.number_input("Enter Target Net Opening (inches)", min_value=1.0, value=100.0)
    target_doors = st.number_input("Enter Number of Doors", min_value=2, max_value=30, value=4)

    best_fit = None
    for label, data in [("23\"", section_data_23), ("30\"", section_data_30)]:
        sections, width = determine_sections_from_doors(target_doors, data)
        if width <= target_width:
            if not best_fit or width > best_fit[1]:
                best_fit = (sections, width, label)

    if best_fit:
        sections, width, door_type = best_fit
        st.subheader("Configuration Result")
        st.write(f"**Use Sections:**")
        st.write("\n".join(f"- {s}" for s in sections))
        st.write(f"**Total Number of Doors:** {target_doors}")
        st.write(f"**Actual Net Opening:** {width} inches")
        st.write(f"**Selected Door Width:** {door_type}")
    else:
        st.error("No valid configuration found.")

else:
    door_count = st.number_input("Enter Number of Doors", min_value=2, max_value=30, value=4)
    door_width = st.radio("Select Door Width", ["23\"", "30\""])
    selected_data = section_data_23 if door_width == "23\"" else section_data_30
    sections, width = determine_sections_from_doors(door_count, selected_data)

    st.subheader("Configuration Result")
    st.write(f"**Use Sections:**")
    st.write("\n".join(f"- {s}" for s in sections))
    st.write(f"**Total Number of Doors:** {door_count}")
    st.write(f"**Actual Net Opening:** {width} inches")
    st.write(f"**Selected Door Width:** {door_width}")

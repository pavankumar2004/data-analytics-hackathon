import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_loader import load_all_data

def run(results, drivers, constructors, races):
    st.title("F1 Driver Movements - Transition Heatmap")

    # Merge race results with race years to sort chronologically per driver
    merged = pd.merge(results, races[['raceId', 'year']], on='raceId', how='left')

    # Compute transitions for each driver
    transitions = []
    for driver, group in merged.groupby('driverId'):
        group = group.sort_values('year')
        # Get the sequence of constructor IDs for the driver
        constructor_sequence = group['constructorId'].tolist()
        # Record a transition if the constructor changes between consecutive races
        for i in range(1, len(constructor_sequence)):
            if constructor_sequence[i] != constructor_sequence[i-1]:
                transitions.append((constructor_sequence[i-1], constructor_sequence[i]))
                
    if not transitions:
        st.error("No driver transitions found in the data.")
        return

    # Create a DataFrame of transitions
    transitions_df = pd.DataFrame(transitions, columns=['From', 'To'])

    # Create a pivot table for the transitions counts
    pivot_table = pd.crosstab(transitions_df['From'], transitions_df['To'])

    st.subheader("Driver Transition Heatmap")
    st.write("This heatmap shows the number of times drivers switched from one constructor to another.")

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    ax.set_xlabel("To Constructor")
    ax.set_ylabel("From Constructor")
    ax.set_title("Driver Transitions Between Constructors")
    st.pyplot(fig)

    # Display top transitions as a table
    st.subheader("Top Driver Transitions")
    transition_counts = transitions_df.value_counts().reset_index(name='Count')
    transition_counts = transition_counts.sort_values('Count', ascending=False)
    
    # Map constructor IDs to names
    cons_names = constructors.set_index('constructorId')['name'].to_dict()
    transition_counts['From'] = transition_counts['From'].map(cons_names)
    transition_counts['To'] = transition_counts['To'].map(cons_names)
    st.dataframe(transition_counts.head(10))

if __name__ == "__main__":
    data = load_all_data('data')
    run(data['results'], data['drivers'], data['constructors'], data['races'])

import streamlit as st


def generate_arithmetic_sequence(first_term, common_difference, num_terms):
    """
    Generate an arithmetic sequence given the first term, common difference, and number of terms.
    
    Args:
        first_term (float): The first term of the sequence
        common_difference (float): The common difference between consecutive terms
        num_terms (int): The number of terms to generate
    
    Returns:
        list: The arithmetic sequence as a list of numbers
    """
    sequence = []
    for n in range(num_terms):
        term = first_term + n * common_difference
        sequence.append(term)
    return sequence

def generate_geometric_sequence(first_term, common_ratio, num_terms):
    """
    Generate a geometric sequence given the first term, common ratio, and number of terms.
    
    Args:
        first_term (float): The first term of the sequence
        common_ratio (float): The common ratio between consecutive terms
        num_terms (int): The number of terms to generate
    
    Returns:
        list: The geometric sequence as a list of numbers
    """
    sequence = []
    for n in range(num_terms):
        term = first_term * (common_ratio ** n)
        sequence.append(term)
    return sequence

def calculate_geometric_sum(first_term, common_ratio, num_terms):
    """
    Calculate the sum of a geometric series.
    
    Args:
        first_term (float): The first term of the sequence
        common_ratio (float): The common ratio between consecutive terms
        num_terms (int): The number of terms in the series
    
    Returns:
        float: The sum of the geometric series
    """
    if common_ratio == 1:
        # If ratio is 1, all terms are the same
        return first_term * num_terms
    else:
        # Use the formula: S_n = a * (1 - r^n) / (1 - r)
        return first_term * (1 - common_ratio ** num_terms) / (1 - common_ratio)


def main():
    # Set page configuration
    st.set_page_config(page_title="Arithmetic Sequence Generator",
                       page_icon="🔢",
                       layout="wide")

    # Main title
    st.title("🔢 Sequence Generator")
    st.write("Generate arithmetic and geometric sequences with custom parameters")

    # Create columns for better layout
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Parameters")
        
        # Sequence type selection
        sequence_type = st.radio(
            "Sequence Type",
            ["Arithmetic", "Geometric"],
            help="Choose between arithmetic or geometric sequence"
        )

        # Input fields for sequence parameters
        first_term = st.number_input(
            "First Term (a₁)",
            value=1.0,
            step=0.1,
            help="The first term of the sequence")

        num_terms = st.number_input(
            "Number of Terms (n)",
            min_value=1,
            max_value=1000,
            value=10,
            step=1,
            help="How many terms to generate (maximum 1000)")

        # Conditional parameters based on sequence type
        common_difference = None
        common_ratio = None
        
        if sequence_type == "Arithmetic":
            common_difference = st.number_input(
                "Common Difference (d)",
                value=1.0,
                step=0.1,
                help="The constant difference between consecutive terms")
            
            # Display formula information
            st.info("**Formula:** aₙ = a₁ + (n-1) × d")
            
            # Show current parameters
            st.write("**Current Parameters:**")
            st.write(f"- First term: {first_term}")
            st.write(f"- Common difference: {common_difference}")
            st.write(f"- Number of terms: {int(num_terms)}")
            
        else:  # Geometric
            common_ratio = st.number_input(
                "Common Ratio (r)",
                value=2.0,
                step=0.1,
                help="The constant ratio between consecutive terms")
            
            # Display formula information
            st.info("**Formula:** aₙ = a₁ × r^(n-1)")
            
            # Show current parameters
            st.write("**Current Parameters:**")
            st.write(f"- First term: {first_term}")
            st.write(f"- Common ratio: {common_ratio}")
            st.write(f"- Number of terms: {int(num_terms)}")

    with col2:
        st.header("Generated Sequence")

        # Input validation
        if num_terms <= 0:
            st.error("Number of terms must be a positive integer!")
            return

        if num_terms > 1000:
            st.error("Number of terms cannot exceed 1000!")
            return

        try:
            # Generate the sequence based on type
            if sequence_type == "Arithmetic":
                sequence = generate_arithmetic_sequence(first_term,
                                                        common_difference,
                                                        int(num_terms))
                sequence_sum = sum(sequence)
            else:  # Geometric
                sequence = generate_geometric_sequence(first_term,
                                                       common_ratio,
                                                       int(num_terms))
                sequence_sum = calculate_geometric_sum(first_term,
                                                       common_ratio,
                                                       int(num_terms))

            # Display sequence statistics
            st.write(f"**Sequence with {int(num_terms)} terms:**")

            # Show sequence in a formatted way
            if num_terms <= 50:
                # For smaller sequences, show all terms in a nice format
                sequence_str = ", ".join([str(term) for term in sequence])
                st.write(f"**Terms:** {sequence_str}")
            else:
                # For larger sequences, show first few and last few terms
                first_terms = sequence[:10]
                last_terms = sequence[-10:]
                first_str = ", ".join([str(term) for term in first_terms])
                last_str = ", ".join([str(term) for term in last_terms])
                st.write(f"**First 10 terms:** {first_str}")
                st.write(f"**...**")
                st.write(f"**Last 10 terms:** {last_str}")

            # Display additional information
            st.write("---")
            col2a, col2b = st.columns(2)

            with col2a:
                st.metric("First Term", sequence[0])
                if sequence_type == "Geometric":
                    st.metric("Sum of Series", sequence_sum)
                else:
                    st.metric("Sum of Sequence", sequence_sum)

            with col2b:
                st.metric("Last Term", sequence[-1])
                st.metric("Range", sequence[-1] - sequence[0])

            # Show the sequence in a table format for better readability
            if st.checkbox("Show sequence in table format"):
                # Create a table with term number and value
                import pandas as pd

                # Limit table display to prevent performance issues
                display_limit = min(100, len(sequence))
                if len(sequence) > display_limit:
                    st.warning(
                        f"Showing first {display_limit} terms in table (sequence has {len(sequence)} terms total)"
                    )

                df = pd.DataFrame({
                    'Term Number (n)':
                    range(1, display_limit + 1),
                    'Term Value (aₙ)':
                    sequence[:display_limit]
                })
                st.dataframe(df, use_container_width=True)

            # Download option for larger sequences
            if num_terms > 20:
                sequence_text = "\n".join(
                    [f"Term {i+1}: {term}" for i, term in enumerate(sequence)])
                
                if sequence_type == "Arithmetic":
                    file_name = f"arithmetic_sequence_{first_term}_{common_difference}_{int(num_terms)}.txt"
                else:
                    file_name = f"geometric_sequence_{first_term}_{common_ratio}_{int(num_terms)}.txt"
                
                st.download_button(
                    label="Download sequence as text file",
                    data=sequence_text,
                    file_name=file_name,
                    mime="text/plain")

        except Exception as e:
            st.error(
                f"An error occurred while generating the sequence: {str(e)}")

    # Add some helpful information at the bottom
    with st.expander("ℹ️ About Sequences"):
        st.write("""
        ## Arithmetic Sequences
        An **arithmetic sequence** is a sequence of numbers where the difference between 
        consecutive terms is constant. This difference is called the **common difference**.
        
        **Formula:** aₙ = a₁ + (n-1) × d
        
        Where:
        - aₙ is the nth term
        - a₁ is the first term
        - d is the common difference
        - n is the term number
        
        **Examples:**
        - 1, 3, 5, 7, 9... (first term = 1, common difference = 2)
        - 10, 7, 4, 1, -2... (first term = 10, common difference = -3)
        
        ## Geometric Sequences
        A **geometric sequence** is a sequence of numbers where each term after the first 
        is found by multiplying the previous term by a constant. This constant is called the **common ratio**.
        
        **Formula:** aₙ = a₁ × r^(n-1)
        
        **Sum Formula:** Sₙ = a₁ × (1 - r^n) / (1 - r) (when r ≠ 1)
        
        Where:
        - aₙ is the nth term
        - a₁ is the first term
        - r is the common ratio
        - n is the term number
        - Sₙ is the sum of the first n terms
        
        **Examples:**
        - 2, 4, 8, 16, 32... (first term = 2, common ratio = 2)
        - 1, 0.5, 0.25, 0.125... (first term = 1, common ratio = 0.5)
        """)


if __name__ == "__main__":
    main()

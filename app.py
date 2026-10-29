import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Inverse Function Calculator",
    page_icon="📈",
    layout="wide"
)

x, y = sp.symbols("x y")


def parse_function(function_text):
    """Parse and validate a mathematical expression."""
    expression = sp.sympify(function_text)

    if not expression.free_symbols.issubset({x}):
        raise ValueError("Only the variable x is allowed.")

    if expression.is_real is False:
        raise ValueError("Please enter a real-valued function.")

    return expression


def calculate_inverse(expression):
    """Find an inverse expression by solving y = f(x) for x."""
    solutions = sp.solve(sp.Eq(y, expression), x)

    if len(solutions) != 1:
        raise ValueError(
            "A unique inverse could not be found. Try a different function."
        )

    inverse = sp.simplify(solutions[0])

    first_check = sp.simplify(expression.subs(x, inverse) - x)
    second_check = sp.simplify(inverse.subs(x, expression) - x)

    return inverse, first_check, second_check


def evaluate_function(expression, values):
    """Evaluate a function numerically for graphing."""
    numeric_function = sp.lambdify(x, expression, modules="numpy")

    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        result = numeric_function(values)

    result = np.asarray(result, dtype=float)

    if result.ndim == 0:
        result = np.full_like(values, result.item())

    result = np.broadcast_to(result, values.shape).copy()
    result[~np.isfinite(result) | (np.abs(result) > 1e5)] = np.nan

    return result


st.title("📈 Inverse Function Calculator")
st.write(
    "Calculate inverse functions, explore the mathematical steps, "
    "and visualize a function alongside its inverse."
)
st.divider()

with st.sidebar:
    st.header("About the Project")
    st.write(
        "An educational tool using symbolic mathematics and graph "
        "visualization to help students understand inverse functions."
    )
    st.subheader("Example Functions")
    st.code("2*x + 4")
    st.code("3*x - 5")
    st.code("x**2")
    st.code("sqrt(x)")
    st.caption("Use Python-style notation: x**2 means x squared.")

st.subheader("Enter Your Function")
function_text = st.text_input(
    "Original function f(x)",
    value="2*x + 4",
    help="Examples: 2*x + 4, 3*x - 5, x**2"
)
graph_range = st.slider(
    "Graph range", min_value=5, max_value=30, value=10
)
calculate_button = st.button(
    "Calculate Inverse", type="primary", use_container_width=True
)

if calculate_button:
    try:
        expression = parse_function(function_text)
        inverse, first_check, second_check = calculate_inverse(expression)

        st.success("Function processed successfully!")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Function")
            st.latex(rf"f(x) = {sp.latex(expression)}")
        with col2:
            st.subheader("Inverse Expression")
            st.latex(rf"f^{{-1}}(x) = {sp.latex(inverse)}")

        st.divider()
        st.subheader("📝 Step-by-Step Solution")

        st.markdown("**Step 1: Write the original function.**")
        st.latex(rf"y = {sp.latex(expression)}")

        st.markdown("**Step 2: Interchange x and y.**")
        swapped_expression = expression.subs(x, y)
        st.latex(rf"x = {sp.latex(swapped_expression)}")

        st.markdown("**Step 3: Solve the equation for y.**")
        st.latex(rf"y = {sp.latex(inverse)}")

        st.markdown("**Step 4: Write the inverse expression.**")
        st.latex(rf"f^{{-1}}(x) = {sp.latex(inverse)}")

        st.divider()
        st.subheader("📊 Function Graphs")

        values = np.linspace(-graph_range, graph_range, 1000)
        original_values = evaluate_function(expression, values)
        inverse_values = evaluate_function(inverse, values)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(values, original_values, label="Original f(x)", linewidth=2)
        ax.plot(values, inverse_values, label="Inverse f⁻¹(x)", linewidth=2)
        ax.plot(values, values, label="Reference line y = x", linestyle="--")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Original Function and Its Inverse")
        ax.grid(True)
        ax.legend()
        ax.set_xlim(-graph_range, graph_range)
        ax.set_ylim(-graph_range, graph_range)
        st.pyplot(fig)
        plt.close(fig)

        st.info(
            "A function and its inverse are reflections across y = x "
            "when the inverse is valid on the selected domains."
        )

        st.divider()
        st.subheader("✅ Inverse Verification")

        st.markdown("**Check 1: f(f⁻¹(x)) = x**")
        st.latex(
            rf"f(f^{{-1}}(x)) - x = {sp.latex(first_check)}"
        )

        st.markdown("**Check 2: f⁻¹(f(x)) = x**")
        st.latex(
            rf"f^{{-1}}(f(x)) - x = {sp.latex(second_check)}"
        )

        if first_check == 0 and second_check == 0:
            st.success("Both inverse identities are satisfied symbolically.")
        else:
            st.warning(
                "The identities could not both be verified symbolically. "
                "Check the domain and range."
            )

        st.caption(
            "These symbolic checks do not prove that a function has a valid "
            "inverse over its entire domain. Domain restrictions may be needed."
        )

    except Exception:
        st.error(
            "Unable to calculate the inverse. Please enter a supported "
            "mathematical expression, such as '2*x + 4' or '3*x - 5'."
        )

st.divider()
st.caption(
    "Inverse Function Calculator & Graph Visualizer | "
    "Built with Python, Streamlit, SymPy, NumPy and Matplotlib"
)

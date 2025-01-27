import os
from graphviz import Digraph


def truncate_label(text, max_length=50):
    """Truncate a label to fit within a reasonable size for Graphviz."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def generate_visualizations(ats_score, strengths, weaknesses, suggestions):
    """
    Generates visualizations for ATS Score, Strengths, Weaknesses, and Suggestions.

    Outputs:
    - Mind map of the results in PNG format.
    """
    # Ensure Kaleido uses a valid temporary directory without spaces
    os.environ["KAL_DIR"] = "/tmp/kaleido"

    # Create the mind map
    mind_map = Digraph("Mind Map", format="png")
    mind_map.attr(rankdir="TB")  # Top-to-bottom layout
    mind_map.node("ATS", f"ATS Score\n{ats_score:.2f}%", shape="circle", color="blue", style="filled", fillcolor="lightblue")

    # Add Strengths node
    mind_map.node("Strengths", "\n".join([truncate_label(s) for s in strengths]), shape="box", color="green", style="filled", fillcolor="lightgreen")

    # Add Weaknesses node
    mind_map.node("Weaknesses", "\n".join([truncate_label(w) for w in weaknesses]), shape="box", color="red", style="filled", fillcolor="lightcoral")

    # Add Suggestions nodes
    for idx, suggestion in enumerate(suggestions, 1):
        suggestion_node = f"Suggestion {idx}"
        mind_map.node(suggestion_node, truncate_label(suggestion), shape="ellipse", color="orange", style="filled", fillcolor="gold")
        mind_map.edge("ATS", suggestion_node, label="Improve")

    # Connect Strengths and Weaknesses to ATS
    mind_map.edge("ATS", "Strengths", label="Positive")
    mind_map.edge("ATS", "Weaknesses", label="Negative")

    # Render the mind map
    try:
        mind_map.render(filename="mind_map", cleanup=True)
        print("Mind map generated: mind_map.png")
    except Exception as e:
        print(f"Error generating mind map: {e}")


# For standalone testing (comment this out when integrated into the main script)
if __name__ == "__main__":
    sample_ats_score = 85.0
    sample_strengths = [
        "Technical skills are clearly listed",
        "Relevant experience is showcased",
        "Quantifiable achievements are mentioned",
        "Key projects are listed"
    ]
    sample_weaknesses = [
        "Lack of specific numbers or metrics",
        "Unconventional format",
        "Limited relevance to the job",
        "No clear career progression"
    ]
    sample_suggestions = [
        "Add quantifiable achievements",
        "Enhance leadership examples",
        "Improve formatting consistency"
    ]
    generate_visualizations(sample_ats_score, sample_strengths, sample_weaknesses, sample_suggestions)

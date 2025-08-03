from graph import create_workflow

workflow = create_workflow()

final_state = workflow.invoke({
        "articles": None,
        "summaries": None,
        "report": None
    })

print("\n=== AI/ML Weekly News Report ===\n")
print(final_state['report'])



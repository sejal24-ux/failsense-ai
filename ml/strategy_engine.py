import pandas as pd


def recommend_strategies(
    payment_method,
    error_source,
    error_reason
):

    strategies = []

    # Bank/network timeout
    if error_reason == "TIMEOUT":

        strategies.append({
            "strategy": "Retry After Delay",
            "score": 0.65,
            "reason":
                "Timeouts may recover after "
                "temporary service degradation."
        })

        strategies.append({
            "strategy": "Offer Alternative Payment",
            "score": 0.80,
            "reason":
                "Alternative payment methods can "
                "bypass the affected path."
        })

        strategies.append({
            "strategy": "Dynamic Routing",
            "score": 0.90,
            "reason":
                "Routing eligible transactions away "
                "from the affected path may reduce failures."
        })

    # Invalid details
    elif error_reason == "INVALID_DETAILS":

        strategies.append({
            "strategy": "Retry After Delay",
            "score": 0.10,
            "reason":
                "Retrying does not normally correct "
                "invalid payment information."
        })

        strategies.append({
            "strategy": "Offer Alternative Payment",
            "score": 0.70,
            "reason":
                "The customer can use another payment method."
        })

        strategies.append({
            "strategy": "Dynamic Routing",
            "score": 0.40,
            "reason":
                "Routing may not solve customer-input errors."
        })

    # Limit exceeded
    elif error_reason == "LIMIT_EXCEEDED":

        strategies.append({
            "strategy": "Retry After Delay",
            "score": 0.15,
            "reason":
                "Retrying immediately may not solve "
                "a transaction-limit issue."
        })

        strategies.append({
            "strategy": "Offer Alternative Payment",
            "score": 0.85,
            "reason":
                "Another payment method may avoid "
                "the affected transaction limit."
        })

        strategies.append({
            "strategy": "Dynamic Routing",
            "score": 0.45,
            "reason":
                "Routing may help only when another "
                "eligible path is available."
        })

    # Network errors
    elif error_reason == "NETWORK_ERROR":

        strategies.append({
            "strategy": "Retry After Delay",
            "score": 0.60,
            "reason":
                "Temporary network problems may recover."
        })

        strategies.append({
            "strategy": "Offer Alternative Payment",
            "score": 0.75,
            "reason":
                "An alternate payment path can bypass "
                "the affected network."
        })

        strategies.append({
            "strategy": "Dynamic Routing",
            "score": 0.85,
            "reason":
                "Alternative routing can reduce dependency "
                "on an affected network path."
        })

    # Generic fallback
    else:

        strategies.append({
            "strategy": "Retry After Delay",
            "score": 0.40,
            "reason":
                "Temporary failures may recover on retry."
        })

        strategies.append({
            "strategy": "Offer Alternative Payment",
            "score": 0.60,
            "reason":
                "Alternative payment methods may recover "
                "otherwise failed transactions."
        })

        strategies.append({
            "strategy": "Dynamic Routing",
            "score": 0.70,
            "reason":
                "Alternative routing may reduce dependency "
                "on the affected path."
        })

    return pd.DataFrame(strategies)


if __name__ == "__main__":

    print("=" * 70)
    print("FAILSENSE AI - STRATEGY INTELLIGENCE")
    print("=" * 70)

    result = recommend_strategies(
        payment_method="UPI",
        error_source="BANK",
        error_reason="TIMEOUT"
    )

    print(
        "\nPossible recovery strategies:"
    )

    print(
        result.to_string(
            index=False
        )
    )

    best = result.loc[
        result["score"].idxmax()
    ]

    print(
        "\n⭐ Recommended:"
    )

    print(
        best["strategy"]
    )

    print(
        "\nReason:"
    )

    print(
        best["reason"]
    )
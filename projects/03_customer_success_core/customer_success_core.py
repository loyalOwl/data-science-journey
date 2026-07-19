client = {
    "client_id": "client_001",
    "company_name": "Север",
    "monthly_spend": 50_000,
    "days_until_renewal": 10,
    "has_critical_issue": False,
}

print(client["company_name"])
print(client["monthly_spend"])
print(client["days_until_renewal"])


def recommend_action(client):
    days = client.get("days_until_renewal")

    if days is None:
        return "Недостаточно данных о продлении"

    if days <= 14:
        return "Скоро продление подписки"
    else:
        return "До продления ещё есть время"


action = recommend_action(client)
print(action)
assert recommend_action({"days_until_renewal": 10}) == "Скоро продление подписки"
assert recommend_action({"days_until_renewal": 20}) == "До продления ещё есть время"
assert recommend_action({"days_until_renewal": 14}) == "Скоро продление подписки"
assert recommend_action({"days_until_renewal": 15}) == "До продления ещё есть время"
assert recommend_action({}) == "Недостаточно данных о продлении"

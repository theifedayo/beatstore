{% load currency_conversions %}
<!-- display balance tagline, estimate in USD and received/sent -->
{% wallet_tagline profile.bitcoin_wallet %}
<!-- display list of transactions as a table -->
{% wallet_history profile.bitcoin_wallet %}
{% load currency_conversions %}
Hi, for the beats: send me {{bitcoin_amount}}BTC (about {{ bitcoin_amount|btc2usd }}USD).

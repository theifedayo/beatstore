{% load currency_conversions %}
<!-- display balance tagline, estimate in USD and received/sent -->
{% wallet_tagline profile.bitcoin_wallet %}
<!-- display list of transactions as a table -->
{% wallet_history profile.bitcoin_wallet %}

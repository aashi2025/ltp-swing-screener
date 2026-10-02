import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from _screener_engine import run_swing_screener, parse_option_chain_data, fetch_nse_option_chain_live, generate_synthetic_option_chain, fetch_live_spot_price, set_broker_token, process_single_stock, BROKER_CONFIG, FO_UNIVERSE
except ImportError:
    try:
        from screener_engine import run_swing_screener, parse_option_chain_data, fetch_nse_option_chain_live, generate_synthetic_option_chain, fetch_live_spot_price, set_broker_token, process_single_stock, BROKER_CONFIG, FO_UNIVERSE
    except ImportError:
        from api._screener_engine import run_swing_screener, parse_option_chain_data, fetch_nse_option_chain_live, generate_synthetic_option_chain, fetch_live_spot_price, set_broker_token, process_single_stock, BROKER_CONFIG, FO_UNIVERSE

app = Flask(__name__, static_folder='../public', static_url_path='')

@app.route('/')
def home():
    public_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public')
    index_file = os.path.join(public_dir, 'index.html')
    if os.path.exists(index_file):
        return send_from_directory(public_dir, 'index.html')
    return "LTP Swing Trading Screener Backend Ready.", 200

@app.route('/api/health')
def health():
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_universe_stocks": len(FO_UNIVERSE),
        "broker_provider": BROKER_CONFIG["api_provider"],
        "token_configured": bool(BROKER_CONFIG["api_token"])
    })

@app.route('/api/config/token', methods=['GET', 'POST'])
def handle_token_config():
    if request.method == 'POST':
        data = request.get_json() or {}
        provider = data.get('provider', 'DEFAULT_HYBRID')
        token = data.get('token', '')
        set_broker_token(provider, token)
        return jsonify({
            "status": "success",
            "message": f"Broker Token updated successfully for provider: {provider}",
            "provider": provider,
            "has_token": bool(token)
        })
    return jsonify({
        "provider": BROKER_CONFIG["api_provider"],
        "has_token": bool(BROKER_CONFIG["api_token"])
    })

@app.route('/api/scan', methods=['GET', 'POST'])
def scan_swing_setups():
    try:
        signal_filter = request.args.get('filter', 'all').upper()
        custom_sym = request.args.get('symbol', '').strip().upper()
        
        if custom_sym and custom_sym not in FO_UNIVERSE:
            target_list = [custom_sym] + FO_UNIVERSE
        else:
            target_list = FO_UNIVERSE

        results = run_swing_screener(target_list)
        
        if signal_filter == 'BULLISH':
            filtered = [r for r in results if r['signal_type'] == 'BULLISH']
        elif signal_filter == 'BEARISH':
            filtered = [r for r in results if r['signal_type'] == 'BEARISH']
        elif signal_filter == 'SIGNALS_ONLY':
            filtered = [r for r in results if r['signal_type'] in ['BULLISH', 'BEARISH']]
        else:
            filtered = results
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().strftime("%b %d, %Y - %I:%M:%S %p"),
            "total_scanned": len(results),
            "filtered_count": len(filtered),
            "bullish_count": len([r for r in results if r['signal_type'] == 'BULLISH']),
            "bearish_count": len([r for r in results if r['signal_type'] == 'BEARISH']),
            "broker_provider": BROKER_CONFIG["api_provider"],
            "stocks": filtered
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/option-chain/<symbol>', methods=['GET'])
def get_option_chain_snapshot(symbol):
    try:
        sym_clean = symbol.upper().strip()
        parsed = process_single_stock(sym_clean)
        return jsonify({
            "status": "success",
            "symbol": sym_clean,
            "timestamp": datetime.now().strftime("%b %d, %Y - %I:%M:%S %p"),
            "data": parsed
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

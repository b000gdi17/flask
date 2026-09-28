from flask import Flask, request, jsonify, render_template
from collections import defaultdict
from pymongo import MongoClient
import time
from datetime import datetime
from database import mycol
from cache_layer import get_cached, set_cache

app = Flask(__name__)

def save_run(endpoint, inp, out, elapsed):
	mycol.insert_one({
		"endpoint": endpoint,
		"timestamp": datetime.now(),
		"input": inp,
		"output": out,
		"elapsed": elapsed
		})

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/slow", methods = ["POST"])
def slow():

	strs_raw = request.get_json()
	strs = [s.lower() for s in strs_raw]

	cached = get_cached(strs)
	if cached:
		return jsonify(cached)

	start = time.time()
	dictionar = {}

	for word in strs:
		dictionar["".join(sorted(word))] = []

	for word in strs:
		cheie = "".join(sorted(word))
		if cheie in dictionar:
			dictionar[cheie].append(word)
	
	result = list(dictionar.values())
	stop = time.time()
	elapsed = stop - start

	set_cache(strs, result)
	save_run("slow", strs_raw, result, elapsed)

	return jsonify(result)

@app.route("/fast", methods = ["POST"])
def fast():

	strs_raw = request.get_json()
	strs = [s.lower() for s in strs_raw]

	cached = get_cached(strs)
	if cached:
		return jsonify(cached)

	start = time.time()
	res = defaultdict(list)

	for s in strs:
		count = [0] * 26
		for c in s:
			count[ord(c) - ord("a")] += 1

		res[tuple(count)].append(s)

	result = list(res.values())
	stop = time.time()
	elapsed = stop - start

	set_cache(strs, result)
	save_run("fast", strs_raw, result, elapsed)

	return jsonify(result)
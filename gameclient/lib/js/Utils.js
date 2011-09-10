// The following line is for JSHint
/*global ImprovedNoise: true */

function _Utils() {
	var self = this;

	/**
	 * Helper method to generate each z for the land object vertices.
	 * 
	 * Taken from a three.js example.
	 */
	this.generateHeight = function(width, height) {
		var size = width * height, data = new Float32Array(size),
		perlin = new ImprovedNoise(), quality = 1, z = 0.9;

		for (var i = 0; i < size; i++) {
			data[i] = 0;
		}

		for (var j = 0; j < 4; j++) {
			for (var k = 0; k < size; k++) {
				var x = k % width, y = ~~ (k / width);
				data[k] += Math.abs(perlin.noise( x / quality, y / quality, z) * quality * 1.75);
			}

			quality *= 5;
		}

		return data;
	};
}

var utils = new _Utils();

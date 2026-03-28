<script lang="ts">
	import { onMount } from 'svelte';
	import * as THREE from 'three';

	let container: HTMLDivElement;

	onMount(() => {
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.1, 100);
		camera.position.set(0, 0.3, 4.5);

		const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
		renderer.setSize(container.clientWidth, container.clientHeight);
		renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
		renderer.toneMapping = THREE.ACESFilmicToneMapping;
		renderer.toneMappingExposure = 1.4;
		container.appendChild(renderer.domElement);

		// Gold metallic liquid blob
		const geometry = new THREE.IcosahedronGeometry(1.6, 128);

		const material = new THREE.ShaderMaterial({
			uniforms: {
				uTime: { value: 0 },
			},
			vertexShader: `
				uniform float uTime;
				varying vec3 vNormal;
				varying vec3 vWorldPos;
				varying vec3 vViewDir;
				varying float vDisp;

				vec3 mod289(vec3 x){ return x - floor(x*(1.0/289.0))*289.0; }
				vec4 mod289(vec4 x){ return x - floor(x*(1.0/289.0))*289.0; }
				vec4 permute(vec4 x){ return mod289(((x*34.0)+1.0)*x); }
				vec4 taylorInvSqrt(vec4 r){ return 1.79284291400159 - 0.85373472095314*r; }

				float snoise(vec3 v){
					const vec2 C = vec2(1.0/6.0, 1.0/3.0);
					const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
					vec3 i = floor(v + dot(v, C.yyy));
					vec3 x0 = v - i + dot(i, C.xxx);
					vec3 g = step(x0.yzx, x0.xyz);
					vec3 l = 1.0 - g;
					vec3 i1 = min(g.xyz, l.zxy);
					vec3 i2 = max(g.xyz, l.zxy);
					vec3 x1 = x0 - i1 + C.xxx;
					vec3 x2 = x0 - i2 + C.yyy;
					vec3 x3 = x0 - D.yyy;
					i = mod289(i);
					vec4 p = permute(permute(permute(
						i.z + vec4(0.0, i1.z, i2.z, 1.0))
						+ i.y + vec4(0.0, i1.y, i2.y, 1.0))
						+ i.x + vec4(0.0, i1.x, i2.x, 1.0));
					float n_ = 0.142857142857;
					vec3 ns = n_ * D.wyz - D.xzx;
					vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
					vec4 x_ = floor(j * ns.z);
					vec4 y_ = floor(j - 7.0 * x_);
					vec4 x = x_ * ns.x + ns.yyyy;
					vec4 y = y_ * ns.x + ns.yyyy;
					vec4 h = 1.0 - abs(x) - abs(y);
					vec4 b0 = vec4(x.xy, y.xy);
					vec4 b1 = vec4(x.zw, y.zw);
					vec4 s0 = floor(b0)*2.0 + 1.0;
					vec4 s1 = floor(b1)*2.0 + 1.0;
					vec4 sh = -step(h, vec4(0.0));
					vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy;
					vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww;
					vec3 p0 = vec3(a0.xy,h.x);
					vec3 p1 = vec3(a0.zw,h.y);
					vec3 p2 = vec3(a1.xy,h.z);
					vec3 p3 = vec3(a1.zw,h.w);
					vec4 norm = taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
					p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
					vec4 m = max(0.6 - vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)), 0.0);
					m = m * m;
					return 42.0 * dot(m*m, vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
				}

				void main(){
					// Slow, organic morphing — layered noise
					float slow = uTime * 0.15;
					float n1 = snoise(position * 0.8 + slow) * 0.22;
					float n2 = snoise(position * 1.6 + slow * 1.3) * 0.10;
					float n3 = snoise(position * 3.2 + slow * 0.7) * 0.04;
					float disp = n1 + n2 + n3;

					vec3 newPos = position + normal * disp;
					vDisp = disp;
					vNormal = normalize(normalMatrix * normal);
					vec4 worldPos = modelMatrix * vec4(newPos, 1.0);
					vWorldPos = worldPos.xyz;
					vViewDir = normalize(cameraPosition - worldPos.xyz);
					gl_Position = projectionMatrix * viewMatrix * worldPos;
				}
			`,
			fragmentShader: `
				uniform float uTime;
				varying vec3 vNormal;
				varying vec3 vWorldPos;
				varying vec3 vViewDir;
				varying float vDisp;

				void main(){
					// Lights
					vec3 light1 = normalize(vec3(2.0, 3.0, 4.0));
					vec3 light2 = normalize(vec3(-3.0, 1.0, -2.0));
					vec3 light3 = normalize(vec3(0.0, -2.0, 3.0));

					vec3 N = normalize(vNormal);
					vec3 V = normalize(vViewDir);
					vec3 H1 = normalize(light1 + V);
					vec3 H2 = normalize(light2 + V);

					// Fresnel
					float fresnel = pow(1.0 - max(dot(V, N), 0.0), 4.0);

					// Gold base colors
					vec3 goldDark = vec3(0.15, 0.10, 0.03);
					vec3 goldMid  = vec3(0.65, 0.45, 0.15);
					vec3 goldLight = vec3(1.0, 0.85, 0.55);
					vec3 goldHighlight = vec3(1.0, 0.95, 0.8);

					// Subtle blue caustic accent
					vec3 blueAccent = vec3(0.1, 0.25, 0.6);
					vec3 tealAccent = vec3(0.05, 0.4, 0.35);

					// Diffuse lighting
					float diff1 = max(dot(N, light1), 0.0);
					float diff2 = max(dot(N, light2), 0.0) * 0.3;
					float diff3 = max(dot(N, light3), 0.0) * 0.15;

					// Specular — tight highlights for metallic look
					float spec1 = pow(max(dot(N, H1), 0.0), 128.0);
					float spec2 = pow(max(dot(N, H2), 0.0), 64.0);
					float specBroad = pow(max(dot(N, H1), 0.0), 16.0);

					// Base color — modulated by viewing angle and displacement
					float colorAngle = dot(N, vec3(0.0, 1.0, 0.0)) * 0.5 + 0.5;
					vec3 baseColor = mix(goldDark, goldMid, diff1 * 0.8 + diff2);
					baseColor = mix(baseColor, goldLight, specBroad * 0.5);

					// Add blue/teal caustics on edges
					baseColor += blueAccent * fresnel * 0.3;
					baseColor += tealAccent * pow(fresnel, 2.0) * smoothstep(-0.1, 0.1, vDisp) * 0.4;

					// Ambient occlusion from displacement
					float ao = smoothstep(-0.2, 0.15, vDisp) * 0.5 + 0.5;

					// Compose
					vec3 ambient = goldDark * 0.3 * ao;
					vec3 diffuse = baseColor * (diff1 * 0.7 + diff2 + diff3) * ao;
					vec3 specular = goldHighlight * spec1 * 1.8 + goldLight * spec2 * 0.6;
					vec3 rim = mix(goldMid, blueAccent, 0.3) * fresnel * 0.5;

					vec3 color = ambient + diffuse + specular + rim;

					// ACES filmic tone mapping
					color = color / (color + vec3(1.0));
					color = pow(color, vec3(0.92));

					gl_FragColor = vec4(color, 0.98);
				}
			`,
			transparent: true,
		});

		const mesh = new THREE.Mesh(geometry, material);
		mesh.position.y = -0.6;
		scene.add(mesh);

		// Sparse ambient particles
		const pCount = 40;
		const pGeom = new THREE.BufferGeometry();
		const pPos = new Float32Array(pCount * 3);
		for (let i = 0; i < pCount; i++) {
			pPos[i*3] = (Math.random() - 0.5) * 10;
			pPos[i*3+1] = (Math.random() - 0.5) * 8;
			pPos[i*3+2] = (Math.random() - 0.5) * 4 - 3;
		}
		pGeom.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
		const pMat = new THREE.PointsMaterial({
			size: 0.008,
			color: 0xd4a574,
			transparent: true,
			opacity: 0.3,
			sizeAttenuation: true
		});
		scene.add(new THREE.Points(pGeom, pMat));

		// Mouse tracking for subtle interaction
		let mx = 0, my = 0;
		const onMove = (e: MouseEvent) => {
			mx = (e.clientX / window.innerWidth - 0.5) * 2;
			my = (e.clientY / window.innerHeight - 0.5) * 2;
		};
		window.addEventListener('mousemove', onMove);

		const clock = new THREE.Clock();
		let raf: number;

		function loop() {
			raf = requestAnimationFrame(loop);
			const t = clock.getElapsedTime();
			material.uniforms.uTime.value = t;

			// Very slow, gentle rotation following mouse
			mesh.rotation.x += (my * 0.08 - mesh.rotation.x) * 0.015;
			mesh.rotation.y += (mx * 0.12 - mesh.rotation.y) * 0.015;
			// Slow autonomous drift
			mesh.rotation.z = Math.sin(t * 0.1) * 0.05;

			renderer.render(scene, camera);
		}
		loop();

		const onResize = () => {
			const w = container.clientWidth;
			const h = container.clientHeight;
			camera.aspect = w / h;
			camera.updateProjectionMatrix();
			renderer.setSize(w, h);
		};
		window.addEventListener('resize', onResize);

		return () => {
			cancelAnimationFrame(raf);
			window.removeEventListener('mousemove', onMove);
			window.removeEventListener('resize', onResize);
			renderer.dispose();
			geometry.dispose();
			material.dispose();
			pGeom.dispose();
			pMat.dispose();
			if (container?.contains(renderer.domElement)) {
				container.removeChild(renderer.domElement);
			}
		};
	});
</script>

<div bind:this={container} class="absolute inset-0 z-0"></div>

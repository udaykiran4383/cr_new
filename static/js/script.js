// const scene = new THREE.Scene();
// const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
// const canvas = document.getElementById('one')
// const renderer = new THREE.WebGLRenderer({canvas:canvas});
// renderer.setSize( window.innerWidth, window.innerHeight );
// // document.body.appendChild( renderer.domElement );

// const geometry = new THREE.TorusKnotGeometry( 20, 7, 300, 20,1,2 );
// const material = new THREE.MeshLambertMaterial();
// const torusKnot = new THREE.Mesh( geometry, material );
// scene.add( torusKnot );
// torusKnot.position.set(50,10,10);

// var light = new THREE.DirectionalLight('white');
// light.position.set(2,5,2).normalize();
// scene.add(light);

// camera.position.z = 110;

// document.addEventListener('mousemove',onDocumentMouseMove)

// let mouseX =0;
// let mouseY =0;

// let targetX =0;
// let targetY =0;

// const windowX = window.innerWidth/2;
// const windowY = window.innerHeight/2;

// function onDocumentMouseMove (event) {
// 	mouseX = (event.clientX - windowX)
// 	mouseY = (event.clientY - windowY)

// }

// // const geometry2 = new THREE.SphereGeometry( 15, 32, 16 );
// // const material2 = new THREE.MeshBasicMaterial( { color: 0xffff00 } );
// // const sphere = new THREE.Mesh( geometry2, material2 );
// // scene.add( sphere );
// // sphere.position.set(0,0,0);

// function animate() {



// 	requestAnimationFrame( animate );

// 	torusKnot.rotation.x += 0.01;
// 	torusKnot.rotation.y += 0.01;

	// torusKnot.rotation.x += 0.5 * (targetY - torusKnot.rotation.x)
	// torusKnot.rotation.y += 0.5 * (targetX - torusKnot.rotation.y)
	// torusKnot.rotation.z += 0.5 * (targetY - torusKnot.rotation.x)


// 	renderer.render( scene, camera );
// };

// animate();


'use strict';


function main() {
    const canvas = document.querySelector('#c');
    const renderer = new THREE.WebGLRenderer({canvas, alpha: true});
  
    function makeScene(elem) {
      const scene = new THREE.Scene();
  
      const fov = 75;
      const aspect = window.innerWidth / window.innerHeight;  // the canvas default
      const near = 0.1;
      const far = 1000;
      const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
      camera.position.set(0, 1, 10);
    
      camera.lookAt(0, 0, 0);
  
      {
        const color = 0xFFFFFF;
        const intensity = 1;
        const light = new THREE.DirectionalLight(color, intensity);
        light.position.set(-1, 2, 4);
        scene.add(light);
      }
  
      return {scene, camera, elem};
    }
  
    function setupScene1() {
      const sceneInfo = makeScene(document.querySelector('#box'));
      const geometry = new THREE.TorusKnotGeometry( 3.5, 1.1, 100, 16 );
      const material = new THREE.MeshLambertMaterial();
      material.color= new THREE.Color("rgb(0, 221, 254)");
      const mesh = new THREE.Mesh(geometry, material);
      sceneInfo.scene.add(mesh);
      sceneInfo.mesh = mesh;
      return sceneInfo;
    }
  
    function setupScene2() {
      const sceneInfo = makeScene(document.querySelector('#box2'));
      const geometry = new THREE.SphereGeometry( 5, 12, 15);

const wireframe = new THREE.WireframeGeometry( geometry );

const line = new THREE.LineSegments( wireframe );
line.material.depthTest = false;
line.material.opacity = 1;
line.material.transparent = true;
line.position.set(5,4,-1);

// scene.add( line );
    //   const radius = .8;
    //   const widthSegments = 4;
    //   const heightSegments = 2;
    //   const geometry = new THREE.SphereBufferGeometry(radius, widthSegments, heightSegments);
    //   const material = new THREE.MeshPhongMaterial({
    //     color: 'blue',
    //     flatShading: true,
    //   });
    //   const mesh = new THREE.Mesh(geometry, material);
      sceneInfo.scene.add(line);
      sceneInfo.mesh = line;
      return sceneInfo;
    }
  
    const sceneInfo1 = setupScene1();
    const sceneInfo2 = setupScene2();
  
    function resizeRendererToDisplaySize(renderer) {
      const canvas = renderer.domElement;
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      const needResize = canvas.width !== width || canvas.height !== height;
      if (needResize) {
        renderer.setSize(width, height, false);
      }
      return needResize;
    }
  
    function rendenerSceneInfo(sceneInfo) {
      const {scene, camera, elem} = sceneInfo;
  
      // get the viewport relative position opf this element
      const {left, right, top, bottom, width, height} =
          elem.getBoundingClientRect();
  
      const isOffscreen =
          bottom < 0 ||
          top > renderer.domElement.clientHeight ||
          right < 0 ||
          left > renderer.domElement.clientWidth;
  
      if (isOffscreen) {
        return;
      }
  
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
  
      const positiveYUpBottom = renderer.domElement.clientHeight - bottom;
      renderer.setScissor(left, positiveYUpBottom, width, height);
      renderer.setViewport(left, positiveYUpBottom, width, height);
  
      renderer.render(scene, camera);
    }
    
    document.addEventListener('mousemove',onDocumentMouseMove)

    let mouseX =0;
    let mouseY =0;

    let targetX =0;
    let targetY =0;

    const windowX = window.innerWidth/2;
    const windowY = window.innerHeight/2;

    function onDocumentMouseMove (event) {
        mouseX = (event.clientX - windowX)
        mouseY = (event.clientY - windowY)

    }

    function render(time) {
      time *= 0.005;
  
      resizeRendererToDisplaySize(renderer);
  
      renderer.setScissorTest(false);
      renderer.clear(true, true);
      renderer.setScissorTest(true);
  
      targetX = mouseX * 0.001;
      targetY = mouseY * 0.001;

      sceneInfo1.mesh.rotation.y = time * .1;
      sceneInfo2.mesh.rotation.y = time * .1;
        
      sceneInfo1.mesh.rotation.x += 0.5 * (targetY - sceneInfo1.mesh.rotation.x);
      sceneInfo1.mesh.rotation.y += 0.5 * (targetX - sceneInfo1.mesh.rotation.y);
      sceneInfo1.mesh.rotation.z += 0.5 * (targetY - sceneInfo1.mesh.rotation.x);

      sceneInfo2.mesh.rotation.x += 0.5 * (targetY - sceneInfo2.mesh.rotation.x);
      sceneInfo2.mesh.rotation.y += 0.5 * (targetX - sceneInfo2.mesh.rotation.y);
      sceneInfo2.mesh.rotation.z += 0.5 * (targetY - sceneInfo2.mesh.rotation.x);
    
      rendenerSceneInfo(sceneInfo1);
      rendenerSceneInfo(sceneInfo2);
  
      requestAnimationFrame(render);
    }
  
    requestAnimationFrame(render);
  }
  
  main();
  
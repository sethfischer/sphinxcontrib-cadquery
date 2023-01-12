const RENDERERS = {};
var ID = 0;

const renderWindow = vtk.Rendering.Core.vtkRenderWindow.newInstance();
const openglRenderWindow = vtk.Rendering.OpenGL.vtkRenderWindow.newInstance();
renderWindow.addView(openglRenderWindow);

const rootContainer = document.createElement('div');
rootContainer.style.position = 'fixed';
rootContainer.style.left = 0;
rootContainer.style.top = 0;
rootContainer.style.pointerEvents = 'none';
rootContainer.style.width = '100%';
rootContainer.style.height = '100%';

openglRenderWindow.setContainer(rootContainer);

const interact_style = vtk.Interaction.Style.vtkInteractorStyleManipulator.newInstance();

const manips = {
  rot: vtk.Interaction.Manipulators.vtkMouseCameraTrackballRotateManipulator.newInstance(),
  pan: vtk.Interaction.Manipulators.vtkMouseCameraTrackballPanManipulator.newInstance(),
  zoom1: vtk.Interaction.Manipulators.vtkMouseCameraTrackballZoomManipulator.newInstance(),
  zoom2: vtk.Interaction.Manipulators.vtkMouseCameraTrackballZoomManipulator.newInstance(),
  roll: vtk.Interaction.Manipulators.vtkMouseCameraTrackballRollManipulator.newInstance(),
};

manips.zoom1.setControl(true);
manips.zoom2.setButton(3);
manips.roll.setShift(true);
manips.pan.setButton(2);

for (var k in manips) {
  {
    interact_style.addMouseManipulator(manips[k]);
  }
};

const interactor = vtk.Rendering.Core.vtkRenderWindowInteractor.newInstance();
interactor.setView(openglRenderWindow);
interactor.initialize();
interactor.setInteractorStyle(interact_style);

document.addEventListener('DOMContentLoaded', function () {
  document.body.appendChild(rootContainer);
});

function updateViewPort(element, renderer) {
  const { innerHeight, innerWidth } = window;
  const { x, y, width, height } = element.getBoundingClientRect();
  const viewport = [
    x / innerWidth,
    1 - (y + height) / innerHeight,
    (x + width) / innerWidth,
    1 - y / innerHeight,
  ];
  renderer.setViewport(...viewport);
}

function recomputeViewports() {
  const rendererElems = document.querySelectorAll('.renderer');
  for (let i = 0; i < rendererElems.length; i++) {
    const elem = rendererElems[i];
    const { id } = elem;
    const renderer = RENDERERS[id];
    updateViewPort(elem, renderer);
  }
  renderWindow.render();
}

function resize() {
  rootContainer.style.width = `${window.innerWidth}px`;
  openglRenderWindow.setSize(window.innerWidth, window.innerHeight);
  recomputeViewports();
}

window.addEventListener('resize', resize);
document.addEventListener('scroll', recomputeViewports);


function enterCurrentRenderer(e) {
  interactor.bindEvents(document.body);
  interact_style.setEnabled(true);
  interactor.setCurrentRenderer(RENDERERS[e.target.id]);
}

function exitCurrentRenderer(e) {
  interactor.setCurrentRenderer(null);
  interact_style.setEnabled(false);
  interactor.unbindEvents();
}


function applyStyle(element) {
  element.classList.add('renderer');
  element.style.width = '100%';
  element.style.height = '100%';
  element.style.display = 'inline-block';
  element.style.boxSizing = 'border';
  return element;
}

window.addEventListener('load', resize);

function render(data, parent_element, ratio) {

  // Initial setup
  const renderer = vtk.Rendering.Core.vtkRenderer.newInstance({ background: [1, 1, 1] });

  // iterate over all children
  for (var el of data) {
    var trans = el.position;
    var rot = el.orientation;
    var rgba = el.color;
    var shape = el.shape;

    // load the inline data
    var reader = vtk.IO.XML.vtkXMLPolyDataReader.newInstance();
    const textEncoder = new TextEncoder();
    reader.parseAsArrayBuffer(textEncoder.encode(shape));

    // setup actor,mapper and add
    const mapper = vtk.Rendering.Core.vtkMapper.newInstance();
    mapper.setInputConnection(reader.getOutputPort());
    mapper.setResolveCoincidentTopologyToPolygonOffset();
    mapper.setResolveCoincidentTopologyPolygonOffsetParameters(0.5, 100);

    const actor = vtk.Rendering.Core.vtkActor.newInstance();
    actor.setMapper(mapper);

    // set color and position
    actor.getProperty().setColor(rgba.slice(0, 3));
    actor.getProperty().setOpacity(rgba[3]);

    actor.rotateZ(rot[2] * 180 / Math.PI);
    actor.rotateY(rot[1] * 180 / Math.PI);
    actor.rotateX(rot[0] * 180 / Math.PI);

    actor.setPosition(trans);

    renderer.addActor(actor);

  };

  //add the container
  const container = applyStyle(document.createElement("div"));
  parent_element.appendChild(container);
  container.addEventListener('mouseenter', enterCurrentRenderer);
  container.addEventListener('mouseleave', exitCurrentRenderer);
  container.id = ID;

  renderWindow.addRenderer(renderer);
  updateViewPort(container, renderer);
  renderer.getActiveCamera().set({ position: [1, -1, 1], viewUp: [0, 0, 1] });
  renderer.resetCamera();

  RENDERERS[ID] = renderer;
  ID++;
};

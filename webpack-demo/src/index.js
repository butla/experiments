import _ from 'lodash';
import './styles/app.css';
import '@fortawesome/fontawesome-free/css/all.css'

function component() {
  const element = document.createElement('div');

  // Lodash, currently included via a script, is required for this line to work
  element.innerHTML = _.join(['Hello', 'webpack'], ' ');

  return element;
}

document.body.appendChild(component());

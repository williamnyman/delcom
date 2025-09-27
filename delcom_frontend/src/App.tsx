/* Main app component */

import AddressBar from './components/AddressBar'
import Subtitle from './components/Subtitle'
import Title from './components/Title'
import Textbar from './components/TextBar'

import SubmitButton from './components/SubmitButton'


function App() {
    return(
      <div className='main-content'>
        <Title />
        <Subtitle />
        <AddressBar />
        <Textbar />
        <SubmitButton />
      </div>


    )
}

export default App

import React from 'react'
import axios from 'axios'
import { saveAs } from 'file-saver'
import factsheets_logo from '../../../img/factsheets_logo.png'

class Sidebar extends React.Component {
  constructor() {
    super()

    this.handleClick = this.handleClick.bind(this)
  }

  handleClick() {

    const data = {
      fund_name: this.props.fundName,
      fund_overview: this.props.fundOverview
    }

    axios.post('/api/fact_sheet', data)
      .then(response => {
        // download fact sheet
        const link = document.createElement('a')
        document.body.appendChild(link)
        link.style = 'display: none'
        link.href = '/api/download_fact_sheet'
        link.click()
        console.log('downloaded')
      })
  }


  render() {
    return (
      <div className="sidebar">
        <div id="sidebar-logo">
          <img src={factsheets_logo} />
        </div>
        <ul>
          <div onClick={this.handleClick}>
            <li>Generate Report</li>
          </div>

          <div>
            <li>Manage Data</li>
          </div>

          <div>
            <li>Report Components</li>
          </div>
        </ul>
      </div>
    )
  }
}

export default Sidebar
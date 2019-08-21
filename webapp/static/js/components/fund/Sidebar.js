import React from 'react'
import axios from 'axios'
import { saveAs } from 'file-saver'

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


    // window.location.href = '/api/fact'

    // const Http = new XMLHttpRequest()
    // const url = '/api/fact_sheet'
    // Http.open('POST', url)
    // Http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Http.send(JSON.stringify(data))


  }


  //   })
  //     .then((response) => {
  //       console.log(response)
  //       axios.post('/api/fact_sheet', {
  //         fund_name: 'CRM',
  //         fund_overview: 'testing from ajax call!'
  //       })
  //     })
  // }

  render() {
    return (
      <div className="nav">
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
---
id: TCID-OP-CSP-REC-CREATE-STRIPE
title: Create stripe cstor pool cluster
sidebar_label: TCID-OP-CSP-REC-CREATE-STRIPE
---
------

### Experiment Metadata

<table>
  <tr>
    <th> TCID </th>
    <th> Type </th>
    <th> Description </th>
  </tr>
  <tr>
    <td> TCID-OP-CSP-REC-CREATE-STRIPE </td>
    <td> CStorPool Recommendation </td>
    <td> Verify creation of stripe cstor pool cluster </td>
  </tr>
</table>

### Prerequisites
- Cluster create setup should be done
- DOP should be installed
- BlockDevices should be detected by NDM

### Details
- Director version 1.9 onwards
- Positive test case

### Steps Performed in the test

- Invoke API to list recommendations
- Invoke API to get capacity based recommendations
- Invoke API to get device based recommendations
- Invoke API to get stripe based cstor pool recommendations
- Invoke API to create stripe cstor pool cluster

### Expected output

- Director should be able to create stripe cstor pool cluster

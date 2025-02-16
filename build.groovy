def buildImage() {
    sh "docker build -t moreflix:1.0 ."   
}

return this
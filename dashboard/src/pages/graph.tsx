import { useState, useEffect, useRef } from 'react';
import { Network } from 'vis-network';
import { DataSet } from 'vis-data';

function parseLabel(node) {
    if (node.label === 'Domain') {
        return node.properties.name;
    }
    if (node.label === 'IPAddress') {
        return node.properties.address;
    }
    if (node.label === 'Location') {
        return `${node.properties.country}, ${node.properties.city}, ${node.properties.region}`;
    }
    if (node.label === 'Hosting') {
        return node.properties.organization;
    }
    if (node.label === 'Registrar') {
        return node.properties.name;
    }
}

function GraphPage({ data }) {
    const containerRef = useRef(null);
    const [selectedNode, setSelectedNode] = useState(null);

    useEffect(() => {
        if (!containerRef.current) return;

        const nodes = new DataSet(
            data.nodes.map((node) => ({
                id: node.id,
                label: parseLabel(node), // show label and properties

                color: {
                    background: '#fff',
                    border: '#000',
                }, // set node color
                font: { size: 16 }, // set font size

                properties: JSON.stringify(node.properties),
            }))
        );

        const edges = new DataSet(
            data.relationships.map((relationship) => ({
                from: relationship.from,
                to: relationship.to,
                arrows: 'to',
                label: relationship.type,
                length: 250,
            }))
        );

        const options = {
            // customize network visualization options here
            nodes: {
                shapeProperties: {
                    borderRadius: 4,
                },
            },
            interaction: {
                hover: true,
                tooltipDelay: 1000,
            },
        };

        const network = new Network(containerRef.current, { nodes, edges }, options);

        network.on('click', (event) => {
            if (event.nodes.length === 1) {
                const nodeId = event.nodes[0];
                const node = nodes.get(nodeId);
                setSelectedNode(node);
            }
        });

        network.on('deselectNode', () => {
            setSelectedNode(null);
        });
    }, [data]);

    return (
        <div ref={containerRef} style={{ width: '100vw', height: '90vh', background: '#F4F4F4' }}>
            {selectedNode && (
                <div
                    style={{
                        position: 'fixed',
                        top: '10vh',
                        left: '10vw',
                        width: '80vw',
                        height: '50vh',
                        backgroundColor: '#fff',
                        border: '1px solid #ccc',
                        overflow: 'scroll',
                        padding: 20,
                        zIndex: 1,
                    }}
                >
                    <h3>{selectedNode.label}</h3>

                    <table>
                        <tbody>
                            {Object.entries(JSON.parse(selectedNode.properties)).map(([key, value]) => (
                                <tr key={key}>
                                    <td>{key}</td>
                                    <td>{value}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export async function getStaticProps() {
    const res = await fetch(`http://overseen:5000/domain`);
    const data = await res.json();

    return {
        props: { data },
    };
}

export default GraphPage;

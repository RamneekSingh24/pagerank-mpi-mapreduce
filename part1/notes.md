d = damping_factor
where N is the number of nodes in the graph.
ln = leaf_nodes
connect each leaf node to all other nodes (ln -> i)

score[i] = d * sum {j \in incoming} (score[j] / outdegree[j]) + (1-d) / N



map 
(u, v) -> (v, score[u]/outdegree[u])

reduce
(v, score) -> sum(score)


